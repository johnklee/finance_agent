# Product Guidelines

## 1. User Experience (UX) Principles
- **Clarity and Simplicity:** The natural language interface should be intuitive. Responses from the agent must be clear, concise, and easy for an individual investor to understand, avoiding overly dense financial jargon where possible.
- **Speed and Responsiveness:** Local data caching should be leveraged to ensure queries return results quickly. The user should not experience significant lag when asking common questions.
- **Reliability:** Data synchronization must be robust. The user needs to trust that the data they are querying is accurate and up-to-date.
- **Transparency:** When the agent uses LLMs for analysis, it should be clear to the user that the insights are AI-generated and should not be taken as definitive financial advice.

## 2. Design and Interaction Style
- **Conversational Tone:** The agent should adopt a helpful, professional, yet accessible tone. It acts as a knowledgeable assistant rather than a rigid system.
- **Structured Output:** When presenting data (like stock screens or historical trends), use clear formatting such as tables, bullet points, or simple charts to make the information digestible.
- **Error Handling:** If a query is misunderstood or data is unavailable, the agent should provide a helpful error message and suggest alternative queries or actions.

## 3. Technical and Architectural Guidelines
- **Modularity:** The system must be designed with extensibility in mind. Adding new data sources (e.g., Alpha Vantage, Polygon) or new markets should require minimal changes to the core agent logic.
- **Data Privacy:** By prioritizing local data storage (SQLite/PostgreSQL), the system inherently protects user query history and portfolio data. This principle should be maintained in future updates.
- **Testability:** Core components, especially data fetching and agent orchestration logic, must be thoroughly tested to ensure reliability.

## 4. Future-Proofing
- **API-First Design:** Even though the initial interface is conversational, the underlying architecture should be structured in a way that easily supports a REST API or Web UI in the future.
