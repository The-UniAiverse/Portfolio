import { NextResponse } from 'next/server'

export async function POST(request: Request) {
    const body = await request.json()
    const { event_type, start_time, invitee } = body

    if (!event_type || !start_time || !invitee || !invitee.email || !invitee.name) {
        return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 })
    }

    const apiKey = process.env.CALENDLY_API_KEY
    if (!apiKey) {
        return NextResponse.json({ error: 'Calendly API key not configured' }, { status: 500 })
    }

    try {
        const response = await fetch('https://api.calendly.com/scheduled_events', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event_type,
                start_time,
                invitee: {
                    email: invitee.email,
                    name: invitee.name,
                    timezone: invitee.timezone || 'UTC',
                    questions_and_answers: invitee.questions_and_answers || []
                }
            }),
        })

        if (!response.ok) {
            const errorData = await response.json()
            return NextResponse.json(errorData, { status: response.status })
        }

        const data = await response.json()
        return NextResponse.json(data)
    } catch (error) {
        console.error('Error booking meeting:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
