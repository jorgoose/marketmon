# Marketmon

A Pokemon-style trading card game where S&P 500 companies become collectible creatures. Real financial data powers every card — market cap becomes HP, free cash flow becomes ATK, and earnings growth becomes GRW.

**Demo:** https://youtu.be/X2-WT0VEIgU?si=AyzIVwa8qtCf-NL4

## Sector Weakness Chart

Each sector type has exactly one weakness and is strong against one other — forming an 11-type cycle. Attacks against a weak type deal **1.5× damage**.

```mermaid
graph LR
    TECH[Technology] -->|disrupts| COMM[Communication<br/>Services]
    COMM -->|undermines| CDEF[Consumer<br/>Defensive]
    CDEF -->|prevents need for| HC[Healthcare]
    HC -->|regulates| IND[Industrials]
    IND -->|replaces| NRG[Energy]
    NRG -->|squeezes| UTIL[Utilities]
    UTIL -->|burdens| RE[Real Estate]
    RE -->|crashes| FIN[Financial<br/>Services]
    FIN -->|restricts| CCYC[Consumer<br/>Cyclical]
    CCYC -->|destabilizes| MAT[Materials]
    MAT -->|constrains| TECH

    style TECH fill:#00c2ff,stroke:#0088b3,color:#000
    style COMM fill:#f97316,stroke:#c45c12,color:#000
    style CDEF fill:#68b77b,stroke:#4e8a5d,color:#000
    style HC fill:#e5457b,stroke:#b8365f,color:#fff
    style IND fill:#d4a017,stroke:#9a7412,color:#000
    style NRG fill:#ff6b1a,stroke:#cc5514,color:#000
    style UTIL fill:#64748b,stroke:#4a5568,color:#fff
    style RE fill:#c2873a,stroke:#96682c,color:#000
    style FIN fill:#2a6dd4,stroke:#1e4e99,color:#fff
    style CCYC fill:#a855f7,stroke:#7c3ab8,color:#fff
    style MAT fill:#a8876a,stroke:#806550,color:#000
```

### Matchup Reasoning

| Attacker | Beats | Why |
|---|---|---|
| **Technology** | Communication Services | Tech platforms absorb and displace traditional telecom/media |
| **Communication Services** | Consumer Defensive | Advertising and social media undermine generic staple brands |
| **Consumer Defensive** | Healthcare | Preventive wellness and OTC health products reduce healthcare dependence |
| **Healthcare** | Industrials | Health/safety regulations and environmental mandates constrain industrial operations |
| **Industrials** | Energy | Manufacturing of renewables and efficiency tech displaces fossil fuel demand |
| **Energy** | Utilities | Energy price spikes crush utility margins — they can't pass costs through fast enough |
| **Utilities** | Real Estate | Rising utility costs and infrastructure constraints burden property operations |
| **Real Estate** | Financial Services | Real estate crashes devastate banks through mortgage defaults and toxic assets |
| **Financial Services** | Consumer Cyclical | Credit tightening and rate hikes choke discretionary spending |
| **Consumer Cyclical** | Materials | Demand volatility and trend shifts destabilize raw material suppliers |
| **Materials** | Technology | Rare earth scarcity and supply chain disruptions constrain tech production |

## Card Stats

| Financial Metric | Card Stat |
|---|---|
| Market Cap | HP |
| Free Cash Flow | ATK |
| Shareholder Equity | DEF |
| Earnings Growth | GRW |
