'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import {
  apiUrl, getHealth, matchJob, renderCoverLetter, writeCoverLetter,
  type CoverLetterResult, type JobMatch, type Letter, type Mode, type CandidateProfile, errorText
} from '@/lib/ai-services'
import { ErrorBanner, inputClass, labelClass, ModeSelector, SourceBadge } from '../ToolUI'
import { cleanProfile } from './ProfileForm'

const DIMENSIONS: { key: 'technical' | 'experience' | 'behavioral' | 'career'; label: string }[] = [
  { key: 'technical', label: 'Skills' },
  { key: 'experience', label: 'Experience' },
  { key: 'behavioral', label: 'Work style' },
  { key: 'career', label: 'Career fit' },
]

const VERDICT_STYLE = { PASS: 'bg-green-100 text-green-800', FLAG: 'bg-amber-100 text-amber-800', FAIL: 'bg-red-100 text-red-800' }

const btn = 'bg-primary hover:bg-primary-light text-secondary px-6 py-3 rounded-full font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed'
const btnOutline = 'border-2 border-primary text-primary px-6 py-3 rounded-full font-semibold hover:bg-primary hover:text-secondary transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed'

function FitResult({ m }: { m: JobMatch }) {
  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        {m.overall !== null ? (
          <div>
            <span className="text-4xl font-bold text-primary">{m.overall}</span>
            <span className="text-primary-dark/50">/100</span>
            <span className="ml-3 font-semibold text-primary-dark">{m.band}</span>
          </div>
        ) : (
          <div>
            <span className="text-4xl font-bold text-primary">{m.scores.technical ?? '—'}{m.scores.technical !== null && m.scores.technical !== undefined && '%'}</span>
            <span className="ml-3 font-semibold text-primary-dark">skills match</span>
          </div>
        )}
        <SourceBadge source={m.source} notice={m.notice} />
      </div>

      {m.overall !== null && (
        <div className="space-y-3">
          {DIMENSIONS.map((d) => (
            <div key={d.key}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-primary-dark">{d.label}</span>
                <span className="font-semibold text-primary">{m.scores[d.key]}</span>
              </div>
              <div className="h-2 bg-primary/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full" style={{ width: `${m.scores[d.key] ?? 0}%` }} />
              </div>
            </div>
          ))}
        </div>
      )}

      {(m.location_verdict || m.language_gate || m.experience_verdict) && (
        <div className="flex flex-wrap gap-2 text-xs font-semibold">
          {m.experience_verdict && <span className={`px-3 py-1 rounded-full ${VERDICT_STYLE[m.experience_verdict]}`}>Experience: {m.experience_verdict}</span>}
          {m.location_verdict && <span className={`px-3 py-1 rounded-full ${VERDICT_STYLE[m.location_verdict]}`}>Location: {m.location_verdict}</span>}
          {m.language_gate && <span className={`px-3 py-1 rounded-full ${VERDICT_STYLE[m.language_gate]}`}>Language: {m.language_gate}</span>}
        </div>
      )}
      {m.experience_note && <p className="text-sm text-primary-dark/70">{m.experience_note}</p>}
      {m.language_note && <p className="text-sm text-amber-700">{m.language_note}</p>}

      {(m.matched_skills.length > 0 || m.missing_skills.length > 0) && (
        <div className="flex flex-wrap gap-2">
          {m.matched_skills.map((s) => <span key={`m-${s}`} className="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">✓ {s}</span>)}
          {m.missing_skills.map((s) => <span key={`x-${s}`} className="px-3 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-700 border border-red-200">{s}</span>)}
        </div>
      )}

      {(m.strengths.length > 0 || m.gaps.length > 0) && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <ul className="space-y-1">{m.strengths.map((s) => <li key={s} className="text-green-700">+ {s}</li>)}</ul>
          <ul className="space-y-1">{m.gaps.map((g) => <li key={g} className="text-red-700">– {g}</li>)}</ul>
        </div>
      )}

      {m.recommended_courses.length > 0 && (
        <div className="bg-gradient-blue rounded-xl p-5 text-secondary">
          <p className="font-semibold mb-3">Close the gap with uniAiverse training</p>
          <ul className="space-y-2">
            {m.recommended_courses.map((c) => (
              <li key={c.id} className="text-sm">
                <Link href="/services/training" className="font-semibold underline underline-offset-4 hover:text-primary-lighter">{c.title}</Link>
                <span className="text-secondary/70"> · {c.hours} hrs · covers {c.covers.join(', ')}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

/** Letter editor: paragraphs are blank-line separated; bullets are one per line. */
function LetterEditor({ letter, onChange }: { letter: Letter; onChange: (l: Letter) => void }) {
  const paras = (xs: string[]) => xs.join('\n\n')
  const split = (s: string) => s.split(/\n\s*\n/).map((x) => x.trim()).filter(Boolean)
  return (
    <div className="space-y-4">
      <div>
        <label htmlFor="cl-salutation" className={labelClass}>Greeting</label>
        <input id="cl-salutation" className={inputClass} value={letter.salutation} onChange={(e) => onChange({ ...letter, salutation: e.target.value })} />
      </div>
      <div>
        <label htmlFor="cl-before" className={labelClass}>Opening paragraphs</label>
        <textarea id="cl-before" rows={6} className={inputClass} defaultValue={paras(letter.paragraphs_before_bullets)}
          onChange={(e) => onChange({ ...letter, paragraphs_before_bullets: split(e.target.value) })} />
      </div>
      <div>
        <label htmlFor="cl-bullets" className={labelClass}>Bullet points (one per line)</label>
        <textarea id="cl-bullets" rows={4} className={inputClass} defaultValue={letter.bullets.join('\n')}
          onChange={(e) => onChange({ ...letter, bullets: e.target.value.split('\n').map((x) => x.trim()).filter(Boolean) })} />
      </div>
      <div>
        <label htmlFor="cl-after" className={labelClass}>Closing paragraphs</label>
        <textarea id="cl-after" rows={5} className={inputClass} defaultValue={paras(letter.paragraphs_after_bullets)}
          onChange={(e) => onChange({ ...letter, paragraphs_after_bullets: split(e.target.value) })} />
      </div>
    </div>
  )
}

export default function JobActions({ jobId, profile }: { jobId: string; profile: CandidateProfile }) {
  const [mode, setMode] = useState<Mode>('rules')
  const [aiAvailable, setAiAvailable] = useState<boolean | null>(null)
  const [fit, setFit] = useState<JobMatch | null>(null)
  const [letter, setLetter] = useState<CoverLetterResult | null>(null)
  const [edited, setEdited] = useState<Letter | null>(null)
  const [notes, setNotes] = useState('')
  const [busy, setBusy] = useState<'fit' | 'letter' | 'pdf' | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getHealth().then((h) => setAiAvailable(h.ai_enhanced_available)).catch(() => setAiAvailable(false))
  }, [])

  const needName = !profile.name.trim()

  async function run<T>(kind: 'fit' | 'letter' | 'pdf', fn: () => Promise<T>, done: (r: T) => void) {
    setError(null)
    setBusy(kind)
    try {
      done(await fn())
    } catch (e) {
      setError(errorText(e))
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className="space-y-8">
      {/* Fit */}
      <div className="space-y-4">
        <ModeSelector mode={mode} onChange={setMode} />
        <button type="button" className={btn} disabled={busy !== null || needName}
          onClick={() => run('fit', () => matchJob(cleanProfile(profile), jobId, mode), setFit)}>
          {busy === 'fit' ? 'Checking…' : 'Check my fit'}
        </button>
        {needName && <p className="text-sm text-primary-dark/60">Add your name in the profile first.</p>}
        {fit && <FitResult m={fit} />}
      </div>

      {/* Cover letter */}
      <div className="border-t border-primary/10 pt-8 space-y-4">
        <h4 className="text-xl font-bold text-primary-dark">Cover letter</h4>
        {aiAvailable === false ? (
          <p className="text-sm text-primary-dark/60">Cover letters are written by our AI model, which isn&apos;t available right now.</p>
        ) : (
          <>
            <div>
              <label htmlFor="cl-notes" className={labelClass}>Anything to emphasise? (optional)</label>
              <input id="cl-notes" maxLength={600} className={inputClass} value={notes} onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. my hackathon win, available from June" />
            </div>
            <button type="button" className={btn} disabled={busy !== null || needName || aiAvailable !== true}
              onClick={() => run('letter', () => writeCoverLetter(cleanProfile(profile), jobId, notes), (r) => { setLetter(r); setEdited(r.letter) })}>
              {busy === 'letter' ? 'Writing and reviewing… (up to a minute)' : letter ? 'Write a new version' : 'Write my cover letter'}
            </button>
          </>
        )}

        {letter && edited && (
          <div className="space-y-5">
            <div className="flex flex-wrap items-center gap-3">
              <SourceBadge source="llm" />
              <span className="text-sm text-primary-dark/60">{letter.word_count} words · {letter.pages} page{letter.pages > 1 ? 's' : ''}</span>
            </div>
            {letter.pages > 1 && <p className="text-sm text-amber-700">This letter runs past one page. Trim it before sending.</p>}
            {letter.review_notes.length > 0 && (
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                <p className="font-semibold text-amber-800 mb-2 text-sm">Reviewer notes: double-check these</p>
                <ul className="list-disc pl-5 text-sm text-amber-800 space-y-1">{letter.review_notes.map((n) => <li key={n}>{n}</li>)}</ul>
              </div>
            )}
            <LetterEditor key={letter.pdf_url} letter={edited} onChange={setEdited} />
            <div className="flex flex-wrap gap-3">
              <a href={apiUrl(letter.pdf_url)} target="_blank" rel="noopener noreferrer" className={btn}>Download PDF</a>
              <button type="button" className={btnOutline} disabled={busy !== null}
                onClick={() => run('pdf', () => renderCoverLetter(cleanProfile(profile), edited), (r) => setLetter({ ...letter, letter: edited, pdf_url: r.pdf_url, pages: r.pages, word_count: r.word_count }))}>
                {busy === 'pdf' ? 'Updating…' : 'Update PDF with my edits'}
              </button>
            </div>
          </div>
        )}
      </div>

      <ErrorBanner error={error} />
    </div>
  )
}
