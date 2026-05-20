import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url)
    const eventTypeUri = searchParams.get('event_type_uri')
    const startTime = searchParams.get('start_time')
    const endTime = searchParams.get('end_time')

    if (!eventTypeUri || !startTime || !endTime) {
        return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 })
    }

    const apiKey = process.env.CALENDLY_API_KEY
    if (!apiKey) {
        return NextResponse.json({ error: 'Calendly API key not configured' }, { status: 500 })
    }

    try {
        const response = await fetch(
            `https://api.calendly.com/event_type_available_times?event_type_uri=${eventTypeUri}&start_time=${startTime}&end_time=${endTime}`,
            {
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                },
            }
        )

        if (!response.ok) {
            const errorData = await response.json()
            return NextResponse.json(errorData, { status: response.status })
        }

        const data = await response.json()
        return NextResponse.json(data)
    } catch (error) {
        console.error('Error fetching available times:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
