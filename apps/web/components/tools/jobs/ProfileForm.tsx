'use client'

import { useEffect, useState } from 'react'
import type { CandidateProfile, WorkEntry } from '@/lib/ai-services'
import { inputClass, labelClass } from '../ToolUI'

const STORAGE_KEY = 'uniaiverse.jobfinder.profile'

export const emptyProfile = (): CandidateProfile => ({
  name: '', email: '', phone: '', link: '', city: '', open_to_relocation: false,
  current_title: '', years_experience: null, work_history: [],
  education: [{ degree: '', institution: '', period: '' }],
  skills: [], experience: '', target_roles: [], career_goals: '', languages: [],
})

const list = (s: string) => s.split(',').map((x) => x.trim()).filter(Boolean)

/** "English (fluent), Hindi (native)" ⇄ [{language, level}] */
const parseLanguages = (s: string) =>
  list(s).map((x) => {
    const m = x.match(/^(.*?)\s*\((.*)\)$/)
    return m ? { language: m[1].trim(), level: m[2].trim() } : { language: x, level: '' }
  })
const showLanguages = (ls: CandidateProfile['languages']) => ls.map((l) => (l.level ? `${l.language} (${l.level})` : l.language)).join(', ')

const MAX_ROLES = 6
const emptyRole = (): WorkEntry => ({ title: '', company: '', period: '', highlights: '' })

/** Drop empty education and work-history rows before sending to the API. */
export function cleanProfile(p: CandidateProfile): CandidateProfile {
  return {
    ...p,
    education: p.education.filter((e) => e.degree.trim()),
    work_history: p.work_history.filter((w) => w.title.trim()),
  }
}

function readSaved(): CandidateProfile | null {
  if (typeof window === 'undefined') return null
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? { ...emptyProfile(), ...JSON.parse(saved) } : null
  } catch {
    return null // storage unavailable: start empty
  }
}

export function useStoredProfile() {
  // The saved profile only appears after the user opens a job, so reading it during the first
  // client render cannot cause a server/client HTML mismatch.
  const [profile, setProfile] = useState<CandidateProfile>(() => readSaved() ?? emptyProfile())
  const [remember, setRemember] = useState(() => readSaved() !== null)

  useEffect(() => {
    try {
      if (remember) localStorage.setItem(STORAGE_KEY, JSON.stringify(profile))
      else localStorage.removeItem(STORAGE_KEY)
    } catch {
      /* ignore */
    }
  }, [profile, remember])

  return { profile, setProfile, remember, setRemember }
}

export default function ProfileForm({ profile, onChange, remember, onRemember }: {
  profile: CandidateProfile
  onChange: (p: CandidateProfile) => void
  remember: boolean
  onRemember: (r: boolean) => void
}) {
  // Comma-separated fields are edited as text and parsed on change, so typing a comma doesn't fight the input.
  const [skills, setSkills] = useState(profile.skills.join(', '))
  const [roles, setRoles] = useState(profile.target_roles.join(', '))
  const [languages, setLanguages] = useState(showLanguages(profile.languages))

  const set = <K extends keyof CandidateProfile>(k: K, v: CandidateProfile[K]) => onChange({ ...profile, [k]: v })
  const setRole = (i: number, patch: Partial<WorkEntry>) =>
    set('work_history', profile.work_history.map((w, j) => (j === i ? { ...w, ...patch } : w)))
  const edu = profile.education[0] ?? { degree: '', institution: '', period: '' }
  const setEdu = (patch: Partial<typeof edu>) => set('education', [{ ...edu, ...patch }, ...profile.education.slice(1)])

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="pf-name" className={labelClass}>Full name *</label>
          <input id="pf-name" maxLength={100} className={inputClass} value={profile.name} onChange={(e) => set('name', e.target.value)} />
        </div>
        <div>
          <label htmlFor="pf-city" className={labelClass}>City</label>
          <input id="pf-city" maxLength={80} className={inputClass} value={profile.city} onChange={(e) => set('city', e.target.value)} placeholder="Pune" />
        </div>
        <div>
          <label htmlFor="pf-email" className={labelClass}>Email</label>
          <input id="pf-email" type="email" maxLength={120} className={inputClass} value={profile.email} onChange={(e) => set('email', e.target.value)} />
        </div>
        <div>
          <label htmlFor="pf-phone" className={labelClass}>Phone</label>
          <input id="pf-phone" maxLength={40} className={inputClass} value={profile.phone} onChange={(e) => set('phone', e.target.value)} />
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="pf-link" className={labelClass}>LinkedIn, GitHub or portfolio</label>
          <input id="pf-link" maxLength={200} className={inputClass} value={profile.link} onChange={(e) => set('link', e.target.value)} />
        </div>
      </div>

      {/* Experience */}
      <div className="border-t border-primary/10 pt-5 space-y-4">
        <h5 className="font-bold text-primary-dark">Experience</h5>
        <div className="grid grid-cols-1 sm:grid-cols-[2fr_1fr] gap-4">
          <div>
            <label htmlFor="pf-title" className={labelClass}>Current or most recent title</label>
            <input id="pf-title" maxLength={100} className={inputClass} value={profile.current_title}
              onChange={(e) => set('current_title', e.target.value)} placeholder="Data Analyst (or 'Student')" />
          </div>
          <div>
            <label htmlFor="pf-years" className={labelClass}>Years of experience</label>
            <input id="pf-years" type="number" min={0} max={60} step="0.5" className={inputClass}
              value={profile.years_experience ?? ''} placeholder="0 if none yet"
              onChange={(e) => set('years_experience', e.target.value === '' ? null : Math.min(60, Math.max(0, Number(e.target.value))))} />
          </div>
        </div>

        {profile.work_history.map((w, i) => (
          <div key={i} className="bg-secondary rounded-xl p-4 border border-primary/10 space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label htmlFor={`wh-title-${i}`} className={labelClass}>Role *</label>
                <input id={`wh-title-${i}`} maxLength={100} className={inputClass} value={w.title} onChange={(e) => setRole(i, { title: e.target.value })} />
              </div>
              <div>
                <label htmlFor={`wh-company-${i}`} className={labelClass}>Company</label>
                <input id={`wh-company-${i}`} maxLength={100} className={inputClass} value={w.company} onChange={(e) => setRole(i, { company: e.target.value })} />
              </div>
              <div>
                <label htmlFor={`wh-period-${i}`} className={labelClass}>Years</label>
                <input id={`wh-period-${i}`} maxLength={40} className={inputClass} value={w.period} onChange={(e) => setRole(i, { period: e.target.value })} placeholder="2021–present" />
              </div>
            </div>
            <div>
              <label htmlFor={`wh-hl-${i}`} className={labelClass}>What you did and achieved</label>
              <textarea id={`wh-hl-${i}`} rows={2} maxLength={800} className={inputClass} value={w.highlights}
                onChange={(e) => setRole(i, { highlights: e.target.value })} placeholder="Led …, cut … by 30%, shipped …" />
            </div>
            <button type="button" onClick={() => set('work_history', profile.work_history.filter((_, j) => j !== i))}
              className="text-red-600 hover:text-red-800 text-sm font-semibold">Remove role</button>
          </div>
        ))}
        <button type="button" disabled={profile.work_history.length >= MAX_ROLES}
          onClick={() => set('work_history', [...profile.work_history, emptyRole()])}
          className="border-2 border-primary text-primary px-5 py-2 rounded-full text-sm font-semibold hover:bg-primary hover:text-secondary transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed">
          + Add a role
        </button>
      </div>

      <div className="border-t border-primary/10 pt-5">
        <h5 className="font-bold text-primary-dark mb-4">Education</h5>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="sm:col-span-1">
          <label htmlFor="pf-degree" className={labelClass}>Degree</label>
          <input id="pf-degree" maxLength={120} className={inputClass} value={edu.degree} onChange={(e) => setEdu({ degree: e.target.value })} placeholder="B.E. Computer Engg." />
        </div>
        <div>
          <label htmlFor="pf-inst" className={labelClass}>College</label>
          <input id="pf-inst" maxLength={120} className={inputClass} value={edu.institution} onChange={(e) => setEdu({ institution: e.target.value })} />
        </div>
        <div>
          <label htmlFor="pf-period" className={labelClass}>Years</label>
          <input id="pf-period" maxLength={40} className={inputClass} value={edu.period} onChange={(e) => setEdu({ period: e.target.value })} placeholder="2022–2026" />
        </div>
      </div>
      </div>

      <div>
        <label htmlFor="pf-skills" className={labelClass}>Skills (comma-separated)</label>
        <input id="pf-skills" className={inputClass} value={skills} placeholder="Python, SQL, React, Git"
          onChange={(e) => { setSkills(e.target.value); set('skills', list(e.target.value).slice(0, 40)) }} />
      </div>
      <div>
        <label htmlFor="pf-exp" className={labelClass}>Projects, internships, certifications and other achievements</label>
        <textarea id="pf-exp" rows={4} maxLength={3000} className={inputClass} value={profile.experience}
          onChange={(e) => set('experience', e.target.value)} placeholder="Side projects, open-source work, certifications, awards…" />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="pf-roles" className={labelClass}>Roles you want</label>
          <input id="pf-roles" className={inputClass} value={roles} placeholder="Backend developer, Data analyst"
            onChange={(e) => { setRoles(e.target.value); set('target_roles', list(e.target.value).slice(0, 8)) }} />
        </div>
        <div>
          <label htmlFor="pf-langs" className={labelClass}>Languages</label>
          <input id="pf-langs" className={inputClass} value={languages} placeholder="English (fluent), Hindi (native)"
            onChange={(e) => { setLanguages(e.target.value); set('languages', parseLanguages(e.target.value).slice(0, 8)) }} />
        </div>
      </div>
      <div>
        <label htmlFor="pf-goals" className={labelClass}>Career goals</label>
        <input id="pf-goals" maxLength={600} className={inputClass} value={profile.career_goals} onChange={(e) => set('career_goals', e.target.value)} />
      </div>

      <div className="flex flex-wrap gap-6 text-sm text-primary-dark/80">
        <label className="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" className="w-5 h-5 accent-[#1E40AF]" checked={profile.open_to_relocation}
            onChange={(e) => set('open_to_relocation', e.target.checked)} />
          Open to relocating
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" className="w-5 h-5 accent-[#1E40AF]" checked={remember} onChange={(e) => onRemember(e.target.checked)} />
          Remember my profile on this device
        </label>
      </div>
      <p className="text-xs text-primary-dark/50">
        Your profile is not stored on our servers. It is sent only when you check your fit or write a cover letter;
        AI-enhanced features share it with our AI provider to generate the result.
      </p>
    </div>
  )
}
