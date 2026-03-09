# APEX Frontend Dashboard

## Architecture
This is a standard Create React App (CRA) template heavily modified with **Tailwind CSS** and **Recharts**.

It operates as "Agent 8: Frontend & Demo Builder". It is responsible for making the abstract Multi-Agent orchestration visually understandable to judges and stakeholders.

## Components
- `App.tsx`: Main Layout. Employs a dark-mode brutalist Enterprise design.
- `useWebSocket.ts`: Simulates live telemetry ingestion. During the hackathon, this pulls from `demo_data.json` so you do not have to run the entire heavy backend stack just to record the video.
- `DashboardOverview.tsx`: Shows live Agent counts and Cost Savings.
- `QueryAnalytics.tsx`: Beautiful Recharts AreaChart showing A2C Model switching algorithms in real-time.
- `ProductionScore.tsx`: A custom SVG SVG-animated circle gauge denoting the Agent 7 CI/CD actuarial score.

## Setup
```bash
cd frontend
npm install
npm start
```
