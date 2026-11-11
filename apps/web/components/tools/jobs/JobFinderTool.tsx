'use client'

import { useEffect, useRef, useState, type FormEvent } from 'react'
import { getJob, searchJobs, type JobCard, type JobDetail, type JobLevel, type JobSearchResult, type WorkMode, errorText } from '@/lib/ai-services'
import { Card, ErrorBanner, inputClass, labelClass, Loading } from '../ToolUI'
import JobActions from './JobActions'
import SignInGate from '@/components/auth/SignInGate'
import ProfileForm, { useStoredProfile } from './ProfileForm'

// Largest Indian job markets in freehire's city facet.
const CITIES = ['Bengaluru', 'Hyderabad', 'Mumbai', 'Pune', 'Chennai', 'Gurugram', 'Noida', 'Delhi', 'Kolkata', 'Ahmedabad', 'Kochi', 'Jaipur', 'Indore']
const LEVELS: { value: JobLevel; label: string }[] = [
  { value: 'any', label: 'Any level' },
  { value: 'entry', label: 'Entry level (intern + junior)' },
  { value: 'intern', label: 'Internships' },
  { value: 'junior', label: 'Junior / fresher' },
  { value: 'mid', label: 'Mid-level' },
  { value: 'senior', label: 'Senior' },
  { value: 'lead', label: 'Lead / staff / principal' },
  { value: 'executive', label: 'Executive' },
]
const PAGE_SIZE = 20
const INITIAL_FILTERS = { q: '', city: '', level: 'any' as JobLevel, work_mode: '' as WorkMode, posted_within_days: 0 }

function JobListItem({ job, active, onClick }: { job: JobCard; active: boolean; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick}
      className={`w-full text-left p-5 rounded-xl border-2 transition-all duration-300 ${
        active ? 'border-primary bg-primary/5 shadow-lg' : 'border-transparent bg-secondary-light hover:border-primary-light hover:shadow-md'
      }`}>
      <div className="font-bold text-primary-dark">{job.title}</div>
      <div className="text-sm text-primary-dark/70 mt-1">{job.company ?? 'Company not listed'}</div>
      <div className="text-xs text-primary-dark/50 mt-1 truncate">{[job.location, job.work_mode, job.date].filter(Boolean).join(' · ')}</div>
      {job.skills.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-3">
          {job.skills.slice(0, 5).map((s) => <span key={s} className="bg-primary/10 text-primary px-2 py-0.5 rounded-full text-xs font-semibold">{s}</span>)}
        </div>
      )}
    </button>
  )
}

export default function JobFinderTool() {
  const [filters, setFilters] = useState(INITIAL_FILTERS)
  const [page, setPage] = useState(1)
  const [results, setResults] = useState<JobSearchResult | null>(null)
  const [searching, setSearching] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<JobDetail | null>(null)
  const [loadingJob, setLoadingJob] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const { profile, setProfile, remember, setRemember } = useStoredProfile()
  const detailRef = useRef<HTMLDivElement>(null)

  async function runSearch(p: number) {
    setError(null)
    setSearching(true)
    try {
      setResults(await searchJobs({ ...filters, page: p }))
      setPage(p)
    } catch (e) {
      setError(errorText(e))
    } finally {
      setSearching(false)
    }
  }

  useEffect(() => {
    let cancelled = false
    searchJobs({ ...INITIAL_FILTERS, page: 1 })
      .then((r) => !cancelled && setResults(r))
      .catch((e) => !cancelled && setError(errorText(e)))
      .finally(() => !cancelled && setSearching(false))
    return () => { cancelled = true }
  }, [])

  async function openJob(id: string) {
    setError(null)
    setLoadingJob(true)
    try {
      setSelected(await getJob(id))
      if (window.innerWidth < 1024) detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } catch (e) {
      setError(errorText(e))
    } finally {
      setLoadingJob(false)
    }
  }

  const submit = (e: FormEvent) => { e.preventDefault(); runSearch(1) }
  const pages = results ? Math.max(1, Math.ceil(results.total / PAGE_SIZE)) : 1
  const flagged = selected?.guard && selected.guard.includes('⚠')

  return (
    <div className="space-y-8">
      {/* Filters */}
      <form onSubmit={submit}>
        <Card className="!p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-[2fr_1fr_1fr_1fr_1fr_auto] gap-4 items-end">
            <div>
              <label htmlFor="jf-q" className={labelClass}>Role or skill</label>
              <input id="jf-q" maxLength={100} className={inputClass} value={filters.q} placeholder="python, data analyst, react…"
                onChange={(e) => setFilters({ ...filters, q: e.target.value })} />
            </div>
            <div>
              <label htmlFor="jf-city" className={labelClass}>City</label>
              <select id="jf-city" className={inputClass} value={filters.city} onChange={(e) => setFilters({ ...filters, city: e.target.value })}>
                <option value="">All India</option>
                {CITIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label htmlFor="jf-level" className={labelClass}>Level</label>
              <select id="jf-level" className={inputClass} value={filters.level} onChange={(e) => setFilters({ ...filters, level: e.target.value as JobLevel })}>
                {LEVELS.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </div>
            <div>
              <label htmlFor="jf-mode" className={labelClass}>Work mode</label>
              <select id="jf-mode" className={inputClass} value={filters.work_mode} onChange={(e) => setFilters({ ...filters, work_mode: e.target.value as WorkMode })}>
                <option value="">Any</option><option value="remote">Remote</option><option value="hybrid">Hybrid</option><option value="onsite">On-site</option>
              </select>
            </div>
            <div>
              <label htmlFor="jf-age" className={labelClass}>Posted</label>
              <select id="jf-age" className={inputClass} value={filters.posted_within_days} onChange={(e) => setFilters({ ...filters, posted_within_days: Number(e.target.value) })}>
                <option value={0}>Any time</option><option value={1}>Last 24 hours</option><option value={7}>Last 7 days</option>
                <option value={14}>Last 14 days</option><option value={30}>Last 30 days</option>
              </select>
            </div>
            <button type="submit" disabled={searching}
              className="bg-primary hover:bg-primary-light text-secondary px-8 py-3 rounded-full font-bold transition-all duration-300 disabled:opacity-60">
              {searching ? 'Searching…' : 'Search'}
            </button>
          </div>
        </Card>
      </form>

      <ErrorBanner error={error} />

      <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,2fr)_minmax(0,3fr)] gap-8 items-start">
        {/* Results */}
        <div className="space-y-3">
          {searching && !results ? <Loading label="Finding jobs…" /> : results && (
            <>
              <p className="text-sm text-primary-dark/60">{results.total.toLocaleString()} jobs found</p>
              {results.results.length === 0 && <p className="text-primary-dark/60 py-8 text-center">No jobs match these filters. Try a wider search.</p>}
              {results.results.map((j) => (
                <JobListItem key={j.id} job={j} active={selected?.id === j.id} onClick={() => openJob(j.id)} />
              ))}
              {pages > 1 && (
                <div className="flex items-center justify-between pt-2">
                  <button type="button" disabled={page <= 1 || searching} onClick={() => runSearch(page - 1)}
                    className="text-primary font-semibold disabled:opacity-30">← Previous</button>
                  <span className="text-sm text-primary-dark/60">Page {page} of {Math.min(pages, 50)}</span>
                  <button type="button" disabled={page >= Math.min(pages, 50) || searching} onClick={() => runSearch(page + 1)}
                    className="text-primary font-semibold disabled:opacity-30">Next →</button>
                </div>
              )}
              <p className="text-xs text-primary-dark/40 pt-2">
                Job listings via <a href={results.attribution.url} target="_blank" rel="noopener noreferrer" className="underline">freehire.me</a>.
              </p>
            </>
          )}
        </div>

        {/* Detail + actions */}
        <div ref={detailRef} className="lg:sticky lg:top-24 space-y-6 scroll-mt-24">
          {loadingJob && <Loading label="Opening job…" />}
          {!loadingJob && !selected && (
            <Card>
              <h3 className="text-2xl font-bold text-primary-dark mb-2">Pick a job to get started</h3>
              <p className="text-primary-dark/70">Open any listing to see the full description, check how well you fit, and get a tailored cover letter.</p>
            </Card>
          )}
          {!loadingJob && selected && (
            <>
              <Card>
                <h3 className="text-2xl font-bold text-primary-dark">{selected.title}</h3>
                <p className="text-primary-dark/70 mt-1">{selected.company ?? 'Company not listed'}</p>
                <p className="text-sm text-primary-dark/50 mt-1">
                  {[selected.location, selected.work_mode, selected.employment_type?.replace('_', ' '), selected.salary].filter(Boolean).join(' · ')}
                </p>
                <div className="flex flex-wrap gap-3 mt-5">
                  {selected.apply_url && (
                    <a href={selected.apply_url} target="_blank" rel="noopener noreferrer nofollow"
                      className="bg-primary hover:bg-primary-light text-secondary px-6 py-2 rounded-full font-semibold transition-all duration-300">Apply on employer site</a>
                  )}
                  <a href={selected.freehire_url} target="_blank" rel="noopener noreferrer"
                    className="border-2 border-primary text-primary px-6 py-2 rounded-full font-semibold hover:bg-primary hover:text-secondary transition-all duration-300">View on freehire</a>
                </div>
                {flagged && (
                  <p className="mt-4 text-sm bg-amber-400/15 border border-amber-400/30 text-amber-300 rounded-lg px-4 py-2">
                    This posting contains hidden or unusual text. It was removed before analysis, but treat the listing with care.
                  </p>
                )}
                {selected.description && (
                  <details className="mt-5 group">
                    <summary className="cursor-pointer text-primary font-semibold">Job description</summary>
                    <p className="mt-3 text-sm text-primary-dark/80 whitespace-pre-line leading-relaxed max-h-96 overflow-y-auto">{selected.description}</p>
                  </details>
                )}
              </Card>

              <Card>
                <button type="button" onClick={() => setProfileOpen(!profileOpen)} className="w-full flex justify-between items-center text-left">
                  <h4 className="text-xl font-bold text-primary-dark">Your profile{profile.name ? `: ${profile.name}` : ''}</h4>
                  <span className="text-primary font-semibold text-sm">{profileOpen ? 'Hide' : profile.name ? 'Edit' : 'Fill in'}</span>
                </button>
                {profileOpen && <div className="mt-6"><ProfileForm profile={profile} onChange={setProfile} remember={remember} onRemember={setRemember} /></div>}
              </Card>

              <Card>
                <SignInGate what="fit checks and cover letters">
                  <JobActions key={selected.id} jobId={selected.id} profile={profile} />
                </SignInGate>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
