<script>
  export let pokemon;
</script>

<div class="card">
  <div class="card-header">
    <h2>{pokemon.name}</h2>
    <span class="hp">{pokemon.hp} HP</span>
  </div>
  
  <div class="card-image">
    <img src={pokemon.imageUrl} alt={pokemon.name} />
  </div>

  <div class="card-body"> 
    <div class="ability">
      <h3>{pokemon.ability.name}</h3>
      <p>{pokemon.ability.description}</p>
    </div>

    <div class="attacks">
      {#each pokemon.attacks as attack}
        <div class="attack">
          <h3>{attack.name}</h3>
          <span class="cost">{attack.cost}</span>
          <p>{attack.description}</p>
        </div>
      {/each}
    </div>
  </div>

  <div class="card-footer">
    <div class="weakness">
      <span class="weakness-value">{pokemon.weakness.value}</span>
      <span class="weakness-type">{pokemon.weakness.type}</span>
    </div>
    <div class="resistance">
      <span class="resistance-value">{pokemon.resistance.value}</span>  
      <span class="resistance-type">{pokemon.resistance.type}</span>
    </div>
    <div class="retreat-cost">
      {#each Array(pokemon.retreatCost) as _}
        <span class="retreat-star">*</span>
      {/each}
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
