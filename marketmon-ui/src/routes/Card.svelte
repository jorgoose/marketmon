<script lang='ts'>
  export let image: string;
  export let name: string;
  export let growth: number;
  export let attack: number;
  export let defense: number;
  export let health: number;
</script>

<div class="card">
  <div class="card-header">
    <h2>{name}</h2>
    <span class="hp">{health} HP</span>
  </div>
  
  <div class="card-image">
    <img src={image} alt={name} />
  </div>

  <div class="card-body"> 
    <div class="ability">
      <h3>Growth</h3>
      <p>{growth}</p>
    </div>

    <div class="attacks">
    <div class="attack">
      <h3>Attack</h3>
      <span class="cost">{attack}</span>
    </div>
    </div>
  </div>

  <div class="card-footer">
    <div class="weakness">
      <span class="weakness-value">Defense</span>
      <span class="weakness-type">{defense}</span>
    </div>
  </div>
</div>

<style>
  .card {
    width: 300px;
    border: 2px solid #8b0000;
    border-radius: 10px;
    background-color: #ffd700;
    padding: 10px;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    background-color: #8b0000;
    padding: 5px;
    color: #fff;
    border-radius: 5px;
  }

  .card-header h2 {
    font-size: 24px;
    margin: 0;
  }

  .hp {
    font-size: 20px;
    font-weight: bold;
  }

  .card-image {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
    background-color: #f0e68c;
    padding: 5px;
    border-radius: 5px;
  }

  .card-image img {
    max-width: 100%;
    max-height: 200px;
  }

  .ability {
    margin-bottom: 10px;
    background-color: #cd853f;
    padding: 5px;
    border-radius: 5px;
    color: #fff;
  }

  .ability h3 {
    font-size: 18px;
    margin: 0;
  }

  .ability p {
    margin: 5px 0;
  }

  .attacks {
    margin-bottom: 10px;
  }

  .attack {
    margin-bottom: 5px;
    background-color: #ff6347;
    padding: 5px;
    border-radius: 5px;
    color: #fff;
  }

  .attack h3 {
    font-size: 16px;
    margin: 0;
    display: inline;
  }

  .cost {
    font-weight: bold;
    margin-left: 5px;
    color: #8b0000;
  }

  .attack p {
    margin: 5px 0;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #8b0000;
    padding: 5px;
    border-radius: 5px;
    color: #fff;
  }

  .weakness,
  .resistance {
    display: flex;
    align-items: center;
  }

  .weakness-value,
  .resistance-value {
    font-size: 18px;
    font-weight: bold;
    margin-right: 5px;
  }

  .weakness-type,
  .resistance-type {
    font-size: 14px;
  }

  .retreat-cost {
    display: flex;
  }

  .retreat-star {
    font-size: 20px;
    color: #ffd700;
    margin-left: 2px;
  }
</style>
