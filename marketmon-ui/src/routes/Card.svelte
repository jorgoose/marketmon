<script lang='ts'>
  export let name: string;
  export let growth: number;
  export let attack: number;
  export let defense: number;
  export let health: number;
  export let company: string;
  export let ticker: string;
  export let sector: string;
  export let image: string = "/creature_images_webp/" + ticker + ".webp";
  export let color: string = '#ffd700';
  export let sizeMultiplier: number = 1.0;

  const sectorColors: { [key: string]: string } = {
    'Industrials': '#d4a017',
    'Healthcare': '#e5457b',
    'Technology': '#00c2ff',
    'Financial Services': '#2a6dd4',
    'Consumer Cyclical': '#a855f7',
    'Communication Services': '#f97316',
    'Consumer Defensive': '#68b77b',
    'Energy': '#ff6b1a',
    'Utilities': '#64748b',
    'Materials': '#a8876a',
    'Real Estate': '#c2873a'
  };

  const sectorBackgrounds: { [key: string]: string } = {
    'Industrials': `
      radial-gradient(ellipse at 30% 18%, rgba(255,255,255,0.22) 0%, transparent 55%),
      repeating-linear-gradient(135deg, transparent, transparent 18px, rgba(255,255,255,0.05) 18px, rgba(255,255,255,0.05) 19px),
      linear-gradient(155deg, #9a7412 0%, #b88c14 22%, #d4a017 48%, #e0b830 72%, #9a7412 100%)
    `,
    'Healthcare': `
      radial-gradient(ellipse at 28% 22%, rgba(255,255,255,0.22) 0%, transparent 50%),
      radial-gradient(circle at 55% 55%, rgba(255,180,200,0.12) 0%, transparent 30%, rgba(255,180,200,0.07) 50%, transparent 65%),
      linear-gradient(155deg, #b8365f 0%, #cc3d6a 25%, #e5457b 48%, #ea6a95 62%, #b8365f 100%)
    `,
    'Technology': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      repeating-linear-gradient(0deg, transparent, transparent 22px, rgba(255,255,255,0.04) 22px, rgba(255,255,255,0.04) 23px),
      repeating-linear-gradient(90deg, transparent, transparent 22px, rgba(255,255,255,0.04) 22px, rgba(255,255,255,0.04) 23px),
      linear-gradient(155deg, #0088b3 0%, #009acc 25%, #00c2ff 50%, #33d1ff 75%, #0088b3 100%)
    `,
    'Financial Services': `
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.22) 0%, transparent 50%),
      repeating-linear-gradient(150deg, transparent, transparent 12px, rgba(255,255,255,0.04) 12px, rgba(255,255,255,0.04) 13px),
      linear-gradient(155deg, #1e4e99 0%, #245dba 25%, #2a6dd4 50%, #4a85e0 75%, #1e4e99 100%)
    `,
    'Consumer Cyclical': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      radial-gradient(circle at 72% 78%, rgba(168,85,247,0.15) 0%, transparent 40%),
      conic-gradient(from 45deg at 50% 50%, transparent 0deg, rgba(255,255,255,0.03) 5deg, transparent 10deg, transparent 80deg, rgba(255,255,255,0.03) 85deg, transparent 90deg, transparent 170deg, rgba(255,255,255,0.03) 175deg, transparent 180deg, transparent 260deg, rgba(255,255,255,0.03) 265deg, transparent 270deg, transparent 350deg, rgba(255,255,255,0.03) 355deg, transparent 360deg),
      linear-gradient(155deg, #7c3ab8 0%, #9045d8 25%, #a855f7 50%, #bb77fa 75%, #7c3ab8 100%)
    `,
    'Communication Services': `
      radial-gradient(ellipse at 28% 20%, rgba(255,255,255,0.2) 0%, transparent 50%),
      radial-gradient(circle at 50% 55%, rgba(255,200,150,0.1) 10%, transparent 25%, rgba(255,200,150,0.06) 40%, transparent 55%, rgba(255,200,150,0.03) 65%, transparent 80%),
      linear-gradient(155deg, #c45c12 0%, #dd6814 25%, #f97316 50%, #fa8c40 75%, #c45c12 100%)
    `,
    'Consumer Defensive': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(90deg, transparent, transparent 20px, rgba(255,255,255,0.03) 20px, rgba(255,255,255,0.03) 21px),
      linear-gradient(155deg, #4e8a5d 0%, #5a9e6a 25%, #68b77b 50%, #80c890 75%, #4e8a5d 100%)
    `,
    'Energy': `
      radial-gradient(ellipse at 50% 38%, rgba(255,180,80,0.2) 0%, transparent 45%),
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.18) 0%, transparent 40%),
      radial-gradient(circle at 50% 100%, rgba(180,60,0,0.25) 0%, transparent 55%),
      linear-gradient(155deg, #cc5514 0%, #e06018 25%, #ff6b1a 50%, #ff8844 75%, #cc5514 100%)
    `,
    'Utilities': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(170deg, transparent, transparent 14px, rgba(255,255,255,0.04) 14px, rgba(255,255,255,0.04) 15px),
      linear-gradient(155deg, #4a5568 0%, #576478 25%, #64748b 50%, #7e8ea0 75%, #4a5568 100%)
    `,
    'Materials': `
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      repeating-linear-gradient(60deg, transparent, transparent 20px, rgba(255,255,255,0.04) 20px, rgba(255,255,255,0.04) 21px),
      repeating-linear-gradient(-60deg, transparent, transparent 20px, rgba(255,255,255,0.03) 20px, rgba(255,255,255,0.03) 21px),
      linear-gradient(155deg, #806550 0%, #946e58 25%, #a8876a 50%, #bca080 75%, #806550 100%)
    `,
    'Real Estate': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(0deg, transparent, transparent 16px, rgba(160,110,50,0.06) 16px, rgba(160,110,50,0.06) 17px),
      repeating-linear-gradient(90deg, transparent, transparent 26px, rgba(160,110,50,0.04) 26px, rgba(160,110,50,0.04) 27px),
      linear-gradient(155deg, #96682c 0%, #ac7832 25%, #c2873a 50%, #d09a50 75%, #96682c 100%)
    `
  };

  const sectorWeaknesses: { [key: string]: string } = {
    'Technology': 'Materials',
    'Communication Services': 'Technology',
    'Consumer Defensive': 'Communication Services',
    'Healthcare': 'Consumer Defensive',
    'Industrials': 'Healthcare',
    'Energy': 'Industrials',
    'Utilities': 'Energy',
    'Real Estate': 'Utilities',
    'Financial Services': 'Real Estate',
    'Consumer Cyclical': 'Financial Services',
    'Materials': 'Consumer Cyclical'
  };

  $: color = sectorColors[sector] || '#ffd700';
  $: cardBg = sectorBackgrounds[sector] || `linear-gradient(155deg, ${color}, ${color})`;
  $: weakness = sectorWeaknesses[sector] || '???';
  $: nameFontSize = name.length > 14 ? '15px' : '18px';
  $: companyFontSize = company.length > 36 ? '9px' : '11px';

</script>

<div class="card-container" style={`zoom: ${sizeMultiplier};`} on:click>
  <div class="card" style="background: {cardBg}">

    <!-- Nameplate -->
    <div class="nameplate">
      <span class="creature-name" style="font-size: {nameFontSize}">{name}</span>
      <span class="creature-hp">{health} <small>HP</small></span>
    </div>

    <!-- Portrait -->
    <div class="portrait">
      <img src={image} alt={name} />
    </div>

    <!-- Info panel -->
    <div class="info-panel">
      <!-- Stats row -->
      <div class="stat-row">
        <div class="stat">
          <span class="stat-val">{growth}</span>
          <span class="stat-lbl">GRW</span>
        </div>
        <div class="stat-sep"></div>
        <div class="stat">
          <span class="stat-val">{attack}</span>
          <span class="stat-lbl">ATK</span>
        </div>
        <div class="stat-sep"></div>
        <div class="stat">
          <span class="stat-val">{defense}</span>
          <span class="stat-lbl">DEF</span>
        </div>
      </div>

      <!-- Type badge -->
      <div class="type-row">
        <span class="type-badge">{sector}</span>
      </div>

      <!-- Card meta -->
      <div class="card-meta">
        <span class="meta-weak">Wk: {weakness}</span>
        <span class="meta-company" style="font-size: {companyFontSize}">{company} ({ticker})</span>
      </div>
    </div>

    <div class="shimmer"></div>
  </div>
</div>

<style>
  .card-container {
    display: inline-block;
    width: 300px;
    aspect-ratio: 63 / 88;
    background: linear-gradient(
      145deg,
      #7a7a8a 0%,
      #b8b8c8 12%,
      #e0e0ea 28%,
      #c8c8d6 45%,
      #e4e4ee 58%,
      #d0d0dc 72%,
      #b8b8c8 88%,
      #7a7a8a 100%
    );
    border-radius: 16px;
    padding: 10px;
    box-shadow:
      2px 3px 12px rgba(0, 0, 0, 0.5),
      inset 0 1px 0 rgba(255, 255, 255, 0.45),
      inset 0 -1px 0 rgba(0, 0, 0, 0.12);
    box-sizing: border-box;
  }

  @media (max-width: 480px) {
    .card-container {
      width: 250px;
    }
  }

  .card {
    position: relative;
    overflow: hidden;
    padding: 8px;
    font-family: 'DM Sans', 'Gill Sans', 'Calibri', sans-serif;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    height: 100%;
    box-sizing: border-box;
  }

  /* ---- Shimmer ---- */
  .shimmer {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      105deg,
      transparent 38%,
      rgba(255, 255, 255, 0.06) 42%,
      rgba(255, 255, 255, 0.14) 50%,
      rgba(255, 255, 255, 0.06) 58%,
      transparent 62%
    );
    transform: translateX(-150%);
    transition: transform 0.65s ease;
    pointer-events: none;
    border-radius: 8px;
    z-index: 3;
  }

  .card-container:hover .shimmer {
    transform: translateX(150%);
  }

  /* ---- Nameplate ---- */
  .nameplate {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 10px;
    background: rgba(0, 0, 0, 0.22);
    border-radius: 6px;
    gap: 6px;
  }

  .creature-name {
    font-weight: 800;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    line-height: 1.2;
    flex: 1;
    min-width: 0;
  }

  .creature-hp {
    font-size: 18px;
    font-weight: 800;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .creature-hp small {
    font-size: 11px;
    font-weight: 700;
    opacity: 0.7;
    letter-spacing: 0.04em;
  }

  /* ---- Portrait ---- */
  .portrait {
    position: relative;
    z-index: 2;
    border-radius: 6px;
    overflow: hidden;
    border: 2px solid rgba(0, 0, 0, 0.25);
    box-shadow:
      inset 0 2px 6px rgba(0, 0, 0, 0.35),
      inset 0 -1px 3px rgba(0, 0, 0, 0.15),
      0 1px 0 rgba(255, 255, 255, 0.08);
    flex: 1;
    min-height: 0;
  }

  .portrait img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* ---- Info panel ---- */
  .info-panel {
    position: relative;
    z-index: 2;
    background: rgba(0, 0, 0, 0.22);
    border-radius: 6px;
    padding: 8px 10px 6px;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  /* ---- Stat row ---- */
  .stat-row {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
  }

  .stat {
    text-align: center;
    flex: 1;
  }

  .stat-val {
    display: block;
    font-size: 20px;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }

  .stat-lbl {
    display: block;
    font-size: 8px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(255, 255, 255, 0.5);
    margin-top: 1px;
  }

  .stat-sep {
    width: 1px;
    height: 24px;
    background: rgba(255, 255, 255, 0.12);
    flex-shrink: 0;
  }

  /* ---- Type badge ---- */
  .type-row {
    text-align: center;
  }

  .type-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(255, 255, 255, 0.8);
    padding: 2px 12px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  /* ---- Card meta ---- */
  .card-meta {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 8px;
    padding-top: 2px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }

  .meta-weak {
    font-size: 9px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.3);
    font-style: italic;
    white-space: nowrap;
  }

  .meta-company {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.45);
    text-align: right;
    line-height: 1.3;
  }
</style>
