import { useState } from 'react'
import './App.css'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function App() {
  const [form, setForm] = useState({
    hcp_name: '', interaction_type: 'Meeting', date: '', time: '',
    attendees: '', topics_discussed: '', materials_shared: '',
    samples_distributed: '', sentiment: 'Neutral', outcomes: '', followup_actions: ''
  })
  const [messages, setMessages] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState('')

  const sendMessage = async () => {
    if (!chatInput.trim()) return
    const userMsg = { role: 'user', text: chatInput }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)
    try {
      const res = await axios.post(`${API_URL}/chat`, { message: chatInput })
      const reply = res.data.response
      setMessages(prev => [...prev, { role: 'ai', text: reply }])
      
      // Extract all fields from AI response
const extract = (label) => {
  const regex = new RegExp(label + '[:\\s]+([^\\n|]+)', 'i')
  const match = reply.match(regex)
  return match ? match[1].trim() : ''
}

const hcp = extract('HCP Name')
const topics = extract('Topics Discussed')
const sentiment = extract('Sentiment')
const materials = extract('(?:Materials Shared|Follow-up Actions|Followup Actions)')
const outcomes = extract('Outcomes')
const followup = extract('Follow-up Actions')
const interactionType = extract('Interaction Type')

if (hcp && hcp.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, hcp_name: hcp }))
setForm(prev => ({ ...prev, date: new Date().toISOString().split('T')[0] }))
if (topics && topics.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, topics_discussed: topics }))
if (outcomes && outcomes.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, outcomes: outcomes }))
const materialsShared = extract('Materials Shared')
if (materialsShared && materialsShared.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, materials_shared: materialsShared }))
if (followup && followup.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, followup_actions: followup }))
if (interactionType && interactionType.toLowerCase() !== 'not mentioned') setForm(prev => ({ ...prev, interaction_type: interactionType }))
if (sentiment.toLowerCase().includes('positive')) setForm(prev => ({ ...prev, sentiment: 'Positive' }))
else if (sentiment.toLowerCase().includes('negative')) setForm(prev => ({ ...prev, sentiment: 'Negative' }))
else if (sentiment.toLowerCase().includes('neutral')) setForm(prev => ({ ...prev, sentiment: 'Neutral' }))
      
      setAiSuggestions(reply)
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: 'Error connecting to AI. Please try again.' }])
    }
    setLoading(false)
    setChatInput('')
  }

 const handleLog = async () => {
  try {
    await axios.post(`${API_URL}/interactions`, {
      hcp_name: form.hcp_name,
      topics_discussed: form.topics_discussed,
      sentiment: form.sentiment,
      outcomes: form.outcomes,
      followup_actions: form.followup_actions
    })
    alert('Interaction logged successfully!')
  } catch (err) {
    alert('Error logging interaction.')
  }
}

  return (
    <div className="app-container">
      <h1 className="app-title">Log HCP Interaction</h1>
      <div className="split-layout">
        
        {/* LEFT - Form Panel */}
        <div className="form-panel">
          <h2>Interaction Details</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label>HCP Name</label>
              <input value={form.hcp_name} onChange={e => setForm({...form, hcp_name: e.target.value})} placeholder="Search or select HCP..." />
            </div>
            <div className="form-group">
              <label>Interaction Type</label>
              <select value={form.interaction_type} onChange={e => setForm({...form, interaction_type: e.target.value})}>
                <option>Meeting</option>
                <option>Call</option>
                <option>Email</option>
                <option>Conference</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Date</label>
              <input type="date" value={form.date} onChange={e => setForm({...form, date: e.target.value})} />
            </div>
            <div className="form-group">
              <label>Time</label>
              <input type="time" value={form.time} onChange={e => setForm({...form, time: e.target.value})} />
            </div>
          </div>

          <div className="form-group">
            <label>Attendees</label>
            <input value={form.attendees} onChange={e => setForm({...form, attendees: e.target.value})} placeholder="Enter names or search..." />
          </div>

          <div className="form-group">
            <label>Topics Discussed</label>
            <textarea value={form.topics_discussed} onChange={e => setForm({...form, topics_discussed: e.target.value})} placeholder="Enter key discussion points..." />
          </div>

          <div className="form-group">
            <label>Materials Shared</label>
            <input value={form.materials_shared} onChange={e => setForm({...form, materials_shared: e.target.value})} placeholder="Search/Add materials..." />
          </div>

          <div className="form-group">
            <label>Samples Distributed</label>
            <input value={form.samples_distributed} onChange={e => setForm({...form, samples_distributed: e.target.value})} placeholder="Add samples..." />
          </div>

          <div className="form-group">
            <label>HCP Sentiment</label>
            <div className="sentiment-group">
              {['Positive', 'Neutral', 'Negative'].map(s => (
                <label key={s} className="sentiment-option">
                  <input type="radio" name="sentiment" value={s} checked={form.sentiment === s} onChange={() => setForm({...form, sentiment: s})} />
                  {s}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Outcomes</label>
            <textarea value={form.outcomes} onChange={e => setForm({...form, outcomes: e.target.value})} placeholder="Key outcomes or agreements..." />
          </div>

          <div className="form-group">
            <label>Follow-up Actions</label>
            <textarea value={form.followup_actions} onChange={e => setForm({...form, followup_actions: e.target.value})} placeholder="Enter next steps or tasks..." />
          </div>
            <button onClick={handleLog} className="log-btn" style={{marginTop: '16px', width: '100%'}}>Save Interaction</button>
          
        </div>

        {/* RIGHT - Chat Panel */}
        <div className="chat-panel">
          <div className="chat-header">
            <span>🤖 AI Assistant</span>
            <p>Log interaction via chat</p>
          </div>
          
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="chat-placeholder">
                <p>Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                {msg.text}
              </div>
            ))}
            {loading && <div className="message ai">Thinking...</div>}
          </div>

          <div className="chat-input-area">
            <textarea
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              placeholder="Describe interaction..."
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
            />
            <button onClick={sendMessage} className="log-btn">Log</button>
          </div>
        </div>

      </div>
    </div>
  )
}

export default App