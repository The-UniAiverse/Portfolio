import { NextResponse } from 'next/server'

export async function GET() {
    const apiKey = process.env.CALENDLY_API_KEY
    if (!apiKey) {
        return NextResponse.json({ error: 'Calendly API key not configured' }, { status: 500 })
    }

    try {
        // First, get the current user to get their organization/user URI
        const userResponse = await fetch('https://api.calendly.com/users/me', {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            },
        })

        if (!userResponse.ok) {
            const errorData = await userResponse.json()
            return NextResponse.json(errorData, { status: userResponse.status })
        }

        const userData = await userResponse.json()
        const userUri = userData.resource.uri

        // Now, get event types for this user
        const eventTypesResponse = await fetch(`https://api.calendly.com/event_types?user=${userUri}`, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            },
        })

        if (!eventTypesResponse.ok) {
            const errorData = await eventTypesResponse.json()
            return NextResponse.json(errorData, { status: eventTypesResponse.status })
        }

        const eventTypesData = await eventTypesResponse.json()
        return NextResponse.json(eventTypesData)
    } catch (error) {
        console.error('Error fetching event types:', error)
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
    }
}
