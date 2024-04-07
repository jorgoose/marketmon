<script lang='ts'>
  export let name: string;
  export let growth: number;
  export let attack: number;
  export let defense: number;
  export let health: number;
  export let company: string;
  export let ticker: string;
  export let sector: string;
  export let image: string = "/creature_images/" + ticker + ".png";
  /* Prop for the card's main color as hex code */
  /* TODO: Add logic to auto-set color based on sector */
  export let color: string = '#ffd700';
  export let sizeMultiplier: number = 1.0;

  /* Map color to sector */
  const sectorColors: { [key: string]: string } = {
    'Industrials': '#ffd700',
    'Healthcare': '#ff7f50',
    'Technology': '#71eaad', // Adjust
    'Financial Services': '#6495ed', //
    'Consumer Cyclical': '#ee82ee', // Make slightly less bright
    'Communication Services': '#ffa07a',
    'Consumer Defensive': '#dda0dd',
    'Energy': '#E26310', // Muted orange
    'Utilities': '#b0c4de',
    'Materials': '#add8e6',
    'Real Estate': '#ffd8b1'
  };

  /* Set the card's color based on sector */
  $: color = sectorColors[sector] || '#ffd700';
  $: companyFontSize = company.length > 38 ? '10px' : '14px';  // Adjust font size based on company name length

</script>

<div class="card-container" style={`transform: scale(${sizeMultiplier});`} on:click>
  <div class="card" style="background-color: {color}">
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
  </div>
</div>

<style>
  .card-container {
    display: inline-block; /* Make cards inline-block */
    width: 300px;
    background: linear-gradient(45deg, #c0c0c0, #ffffff, #c0c0c0);
    border-radius: 20px;
    padding: 10px;
    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.6);
    transform-origin: top left; /* Ensure scaling originates from top left */
  }

  .card {
    /* background-color: #ffd700; */
    padding: 8px;
    font-family: 'Lato', 'Gill Sans', 'Calibri', sans-serif;
    border-radius: 10px;
  }

  .card-header {
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
    border: 5pxs outset;
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