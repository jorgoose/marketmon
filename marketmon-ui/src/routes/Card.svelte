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
  /* Prop for the card's main color as hex code */
  export let color: string = '#ffd700';
  export let sizeMultiplier: number = 1.0;

  /* Map color to sector */
  const sectorColors: { [key: string]: string } = {
    'Industrials': '#ffd700',
    'Healthcare': '#ff7f50',
    'Technology': '#71eaad',
    'Financial Services': '#6495ed',
    'Consumer Cyclical': '#ee82ee',
    'Communication Services': '#ffa07a',
    'Consumer Defensive': '#dda0dd',
    'Energy': '#E26310',
    'Utilities': '#b0c4de',
    'Materials': '#add8e6',
    'Real Estate': '#ffd8b1'
  };

  /* Rich multi-layer backgrounds per sector (Pokemon-style energy patterns) */
  const sectorBackgrounds: { [key: string]: string } = {
    'Industrials': `
      radial-gradient(ellipse at 30% 18%, rgba(255,255,255,0.22) 0%, transparent 55%),
      repeating-linear-gradient(135deg, transparent, transparent 18px, rgba(255,255,255,0.05) 18px, rgba(255,255,255,0.05) 19px),
      linear-gradient(155deg, #9a7b1c 0%, #c9a84c 22%, #ffd700 48%, #daa520 72%, #9a7b1c 100%)
    `,
    'Healthcare': `
      radial-gradient(ellipse at 28% 22%, rgba(255,255,255,0.22) 0%, transparent 50%),
      radial-gradient(circle at 55% 55%, rgba(255,200,180,0.12) 0%, transparent 30%, rgba(255,200,180,0.07) 50%, transparent 65%),
      linear-gradient(155deg, #cc5530 0%, #e86a42 25%, #ff7f50 48%, #ff9068 62%, #cc5530 100%)
    `,
    'Technology': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      repeating-linear-gradient(0deg, transparent, transparent 22px, rgba(255,255,255,0.04) 22px, rgba(255,255,255,0.04) 23px),
      repeating-linear-gradient(90deg, transparent, transparent 22px, rgba(255,255,255,0.04) 22px, rgba(255,255,255,0.04) 23px),
      linear-gradient(155deg, #3a9a74 0%, #55c092 25%, #71eaad 50%, #55c092 75%, #3a9a74 100%)
    `,
    'Financial Services': `
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.22) 0%, transparent 50%),
      repeating-linear-gradient(150deg, transparent, transparent 12px, rgba(255,255,255,0.04) 12px, rgba(255,255,255,0.04) 13px),
      linear-gradient(155deg, #3a6cc7 0%, #5080da 25%, #6495ed 50%, #5080da 75%, #3a6cc7 100%)
    `,
    'Consumer Cyclical': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      radial-gradient(circle at 72% 78%, rgba(200,100,220,0.15) 0%, transparent 40%),
      conic-gradient(from 45deg at 50% 50%, transparent 0deg, rgba(255,255,255,0.03) 5deg, transparent 10deg, transparent 80deg, rgba(255,255,255,0.03) 85deg, transparent 90deg, transparent 170deg, rgba(255,255,255,0.03) 175deg, transparent 180deg, transparent 260deg, rgba(255,255,255,0.03) 265deg, transparent 270deg, transparent 350deg, rgba(255,255,255,0.03) 355deg, transparent 360deg),
      linear-gradient(155deg, #c050c0 0%, #dd6add 25%, #ee82ee 50%, #dd6add 75%, #c050c0 100%)
    `,
    'Communication Services': `
      radial-gradient(ellipse at 28% 20%, rgba(255,255,255,0.2) 0%, transparent 50%),
      radial-gradient(circle at 50% 55%, rgba(255,220,200,0.1) 10%, transparent 25%, rgba(255,220,200,0.06) 40%, transparent 55%, rgba(255,220,200,0.03) 65%, transparent 80%),
      linear-gradient(155deg, #d07048 0%, #e88a62 25%, #ffa07a 50%, #e88a62 75%, #d07048 100%)
    `,
    'Consumer Defensive': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(90deg, transparent, transparent 20px, rgba(255,255,255,0.03) 20px, rgba(255,255,255,0.03) 21px),
      linear-gradient(155deg, #b878b8 0%, #ca90ca 25%, #dda0dd 50%, #ca90ca 75%, #b878b8 100%)
    `,
    'Energy': `
      radial-gradient(ellipse at 50% 38%, rgba(255,200,100,0.2) 0%, transparent 45%),
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.18) 0%, transparent 40%),
      radial-gradient(circle at 50% 100%, rgba(160,50,0,0.25) 0%, transparent 55%),
      linear-gradient(155deg, #a04808 0%, #c25810 25%, #e26310 50%, #c25810 75%, #a04808 100%)
    `,
    'Utilities': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(170deg, transparent, transparent 14px, rgba(255,255,255,0.04) 14px, rgba(255,255,255,0.04) 15px),
      linear-gradient(155deg, #8a9eb8 0%, #9cb0ca 25%, #b0c4de 50%, #9cb0ca 75%, #8a9eb8 100%)
    `,
    'Materials': `
      radial-gradient(ellipse at 28% 18%, rgba(255,255,255,0.2) 0%, transparent 50%),
      repeating-linear-gradient(60deg, transparent, transparent 20px, rgba(255,255,255,0.04) 20px, rgba(255,255,255,0.04) 21px),
      repeating-linear-gradient(-60deg, transparent, transparent 20px, rgba(255,255,255,0.03) 20px, rgba(255,255,255,0.03) 21px),
      linear-gradient(155deg, #82b8cc 0%, #98c8da 25%, #add8e6 50%, #98c8da 75%, #82b8cc 100%)
    `,
    'Real Estate': `
      radial-gradient(ellipse at 25% 18%, rgba(255,255,255,0.18) 0%, transparent 50%),
      repeating-linear-gradient(0deg, transparent, transparent 16px, rgba(180,130,80,0.06) 16px, rgba(180,130,80,0.06) 17px),
      repeating-linear-gradient(90deg, transparent, transparent 26px, rgba(180,130,80,0.04) 26px, rgba(180,130,80,0.04) 27px),
      linear-gradient(155deg, #d0a878 0%, #e0bc96 25%, #ffd8b1 50%, #e0bc96 75%, #d0a878 100%)
    `
  };

  $: color = sectorColors[sector] || '#ffd700';
  $: cardBg = sectorBackgrounds[sector] || `linear-gradient(155deg, ${color}, ${color})`;
  $: companyFontSize = company.length > 38 ? '10px' : '14px';

</script>

<div class="card-container" style={`transform: scale(${sizeMultiplier});`} on:click>
  <div class="card" style="background: {cardBg}">
    <div class="card-header">
      <h2>{name}</h2>
      <span class="hp"><small>HP</small> {health}</span>
    </div>

    <div class="card-image">
      <img src={image} alt={name} />
    </div>

    <div class="card-body">
      <div class="abilities">
        <div class="ability">
          <div class="ability-circle">
            <h3>{growth}</h3>
          </div>
          <p>Growth</p>
        </div>

        <div class="ability">
          <div class="ability-circle">
            <h3>{attack}</h3>
          </div>
          <p>Attack</p>
        </div>

        <div class="ability">
          <div class="ability-circle">
            <h3>{defense}</h3>
          </div>
          <p>Defense</p>
        </div>
      </div>

      <div class="sector-box">
        {sector}
      </div>

      <div class="card-footer">
        <div class="footer-right">
          <div class="weakness italic">Weakness: {sector}</div>
          <div class="company-info" style={`font-size: ${companyFontSize};`}>
            <div>{company} ({ticker})</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Holographic shimmer overlay -->
    <div class="shimmer"></div>
  </div>
</div>

<style>
  .card-container {
    display: inline-block;
    width: 300px;
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
    border-radius: 20px;
    padding: 10px;
    box-shadow:
      3px 3px 12px rgba(0, 0, 0, 0.5),
      inset 0 1px 0 rgba(255, 255, 255, 0.4),
      inset 0 -1px 0 rgba(0, 0, 0, 0.15);
    transform-origin: top left;
  }

  .card {
    position: relative;
    overflow: hidden;
    padding: 8px;
    font-family: 'Lato', 'Gill Sans', 'Calibri', sans-serif;
    border-radius: 10px;
  }

  /* Holographic shimmer sweep on hover */
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
    border-radius: 10px;
    z-index: 1;
  }

  .card-container:hover .shimmer {
    transform: translateX(150%);
  }

  .card-header {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    background-color: transparent;
    color: black;
  }

  .card-header h2 {
    font-size: 20px;
    margin: 0;
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 2px 5px;
    border-radius: 5px;
  }

  .card-header .hp {
    font-size: 20px;
    margin: 0;
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 2px 5px;
    border-radius: 5px;
  }

  .card-header .hp small {
    font-size: 14px;
  }

  .card-image {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
    border: 5px silver outset;
    padding: 2px;
    border-radius: 10px;
  }

  .card-image img {
    height: 200px;
    object-fit: cover;
  }

  .card-body {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .abilities {
    display: flex;
    justify-content: space-evenly;
  }

  .ability {
    text-align: center;
  }

  .ability-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #fff;
    border: 4px silver outset;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
  }

  .ability h3 {
    font-size: 20px;
    margin: 0;
    font-weight: bold;
    color: black;
  }

  .ability p {
    font-size: 14px;
    margin: 5px 0;
    font-weight: bold;
    color: black;
  }

  .sector-box {
    text-align: center;
    font-weight: bold;
    margin-top: 10px;
    font-size: 18px;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 5px;
    border-radius: 10px;
    color: black;
  }

  .card-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 5px;
  }

  .footer-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }

  .weakness,
  .company-info {
    color: black;
    font-weight: bold;
    font-size: 12px;
  }

  .company-info {
    font-size: 14px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }
</style>
