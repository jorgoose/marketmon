<script lang='ts'>
  export let image: string;
  export let name: string;
  export let growth: number;
  export let attack: number;
  export let defense: number;
  export let health: number;
  export let company: string;
  export let ticker: string;
  export let sector: string;
</script>

<div class="card" on:click>
  <div class="card-header">
    <h2>{name}</h2>
    <span class="hp">{health} HP</span>
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
      <div class="weakness">Weakness: Utilities</div>
      <div class="company-info">{company} ({ticker})</div>
    </div>
  </div>
</div>

<style>
  .card {
    width: 300px;
    border: 5px solid silver;
    border-radius: 20px;
    background-color: #ffd700;
    padding: 8px;
    font-family: 'Lato', 'Gill Sans', 'Calibri', sans-serif;
    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.6);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    background-color: transparent;
    color: black;
  }

  .card-header h2,
  .card-header .hp {
    font-size: 20px;
    margin: 0;
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 2px 5px;
    border-radius: 5px;
  }

  .card-image {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
    border: 5px yellow outset;
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
    border: 5px solid silver;
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
    justify-content: space-between;
    align-items: center;
    margin-top: 5px;
  }

  .weakness,
  .company-info {
    color: black;
    font-weight: bold;
    font-size: 12px;
  }
</style>