interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  change?: string
  changeType?: 'up' | 'down' | 'neutral'
  color?: 'blue' | 'purple' | 'green' | 'orange'
}

const colorMap = {
  blue: 'bg-blue-600/20 text-blue-400 border-blue-600/30',
  purple: 'bg-purple-600/20 text-purple-400 border-purple-600/30',
  green: 'bg-emerald-600/20 text-emerald-400 border-emerald-600/30',
  orange: 'bg-orange-600/20 text-orange-400 border-orange-600/30',
}

export default function StatsCard({ title, value, icon, change, changeType = 'neutral', color = 'blue' }: StatsCardProps) {
  return (
    <div className="bg-[#1E293B] border border-blue-900/30 rounded-2xl p-6 hover:border-blue-700/50 transition-all duration-300">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm font-medium mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {change && (
            <p className={`text-xs mt-2 font-medium ${
              changeType === 'up' ? 'text-emerald-400' :
              changeType === 'down' ? 'text-red-400' :
              'text-slate-400'
            }`}>
              {changeType === 'up' ? '↑' : changeType === 'down' ? '↓' : '•'} {change}
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl border flex items-center justify-center ${colorMap[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}
