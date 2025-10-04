import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { amount, description } = await req.json()
    
    let result
    if (description) {
      // Parse existing description
      result = parseExpenseText(description)
    } else {
      // Generate from transaction data
      result = generateFromTransaction(amount)
    }
    
    return new Response(
      JSON.stringify(result),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      },
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400,
      },
    )
  }
})

function generateFromTransaction(amount: number) {
  // Simulate transaction data based on amount patterns
  const transactions = [
    // Food
    { range: [3, 8], businesses: ['Starbucks', 'Dunkin', 'Local Cafe'], category: 'Food', type: 'Coffee' },
    { range: [8, 20], businesses: ['McDonald\'s', 'Subway', 'Chipotle', 'Taco Bell'], category: 'Food', type: 'Fast Food' },
    { range: [20, 60], businesses: ['Olive Garden', 'Applebee\'s', 'Local Restaurant'], category: 'Food', type: 'Restaurant' },
    
    // Transport
    { range: [5, 15], businesses: ['Uber', 'Lyft', 'Local Taxi'], category: 'Transport', type: 'Rideshare' },
    { range: [30, 80], businesses: ['Shell', 'Exxon', 'BP'], category: 'Transport', type: 'Gas Station' },
    
    // Shopping
    { range: [10, 50], businesses: ['Amazon', 'Target', 'Walmart'], category: 'Shopping', type: 'Retail' },
    { range: [50, 200], businesses: ['Best Buy', 'Apple Store', 'Electronics Store'], category: 'Shopping', type: 'Electronics' },
    
    // Entertainment
    { range: [10, 20], businesses: ['AMC Theaters', 'Regal Cinema', 'Local Theater'], category: 'Entertainment', type: 'Movies' },
    { range: [8, 15], businesses: ['Netflix', 'Spotify', 'Disney+'], category: 'Entertainment', type: 'Streaming' },
    
    // Utilities
    { range: [50, 150], businesses: ['Electric Company', 'Water Dept', 'Internet Provider'], category: 'Utilities', type: 'Bills' }
  ]

  // Find matching transaction type based on amount
  const matches = transactions.filter(t => amount >= t.range[0] && amount <= t.range[1])
  const transaction = matches[Math.floor(Math.random() * matches.length)] || 
                     { businesses: ['Unknown Merchant'], category: 'Other', type: 'Purchase' }

  const business = transaction.businesses[Math.floor(Math.random() * transaction.businesses.length)]
  
  return {
    category: transaction.category,
    description: `${transaction.type} - ${business}`,
    amount: amount,
    date: new Date().toISOString(),
    generated: true
  }
}

function parseExpenseText(text: string) {
  const result = {
    category: 'Other',
    amount: null,
    date: null,
    description: text,
    generated: false
  }

  // Extract amount
  const amountMatch = text.match(/\$?(\d+(?:\.\d{2})?)/)
  if (amountMatch) {
    result.amount = parseFloat(amountMatch[1])
  }

  // Extract dates
  const datePatterns = [
    { pattern: /\b(today|now)\b/gi, offset: 0 },
    { pattern: /\b(yesterday)\b/gi, offset: -1 },
    { pattern: /\b(tomorrow)\b/gi, offset: 1 },
    { pattern: /\b(monday)\b/gi, day: 1 },
    { pattern: /\b(tuesday)\b/gi, day: 2 },
    { pattern: /\b(wednesday)\b/gi, day: 3 },
    { pattern: /\b(thursday)\b/gi, day: 4 },
    { pattern: /\b(friday)\b/gi, day: 5 },
    { pattern: /\b(saturday)\b/gi, day: 6 },
    { pattern: /\b(sunday)\b/gi, day: 0 }
  ]

  for (const { pattern, offset, day } of datePatterns) {
    const match = pattern.exec(text)
    if (match) {
      let targetDate = new Date()
      if (offset !== undefined) {
        targetDate.setDate(targetDate.getDate() + offset)
      } else if (day !== undefined) {
        const currentDay = targetDate.getDay()
        const daysUntil = (day - currentDay + 7) % 7
        targetDate.setDate(targetDate.getDate() + (daysUntil || 7))
      }
      result.date = targetDate.toISOString()
      break
    }
  }

  // Categorize
  const keywords = {
    'Food': ['restaurant', 'lunch', 'dinner', 'coffee', 'starbucks', 'mcdonalds', 'food', 'eat'],
    'Transport': ['uber', 'taxi', 'gas', 'fuel', 'parking', 'transport'],
    'Shopping': ['amazon', 'store', 'shopping', 'buy', 'purchase'],
    'Entertainment': ['movie', 'netflix', 'game', 'entertainment'],
    'Health': ['doctor', 'pharmacy', 'medical'],
    'Utilities': ['electric', 'water', 'internet', 'bill']
  }
  
  const lowerText = text.toLowerCase()
  for (const [category, words] of Object.entries(keywords)) {
    if (words.some(word => lowerText.includes(word))) {
      result.category = category
      break
    }
  }

  return result
}
