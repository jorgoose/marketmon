<script lang='ts'>
  export let image: string;
  export let name: string;
  export let growth: number;
  export let attack: number;
  export let defense: number;
  export let health: number;
  export let company: string;
  export let ticker: string;
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
          <h3>GRW</h3>
          <p>{growth}</p>
      </div>
      <div class="ability attack">
          <h3>ATK</h3>
          <p>{attack}</p>
      </div>
      <div class="ability defense">
          <h3>DEF</h3>
          <p>{defense}</p>
      </div>
    </div>
    <div class="weakness">Weakness: Utilities</div>
    <div class="company-info">Caterpillar (CAT)</div>
  </div>
</div>

<style>
.card {
  width: 300px;
  border: 5px solid silver; /* Added silver border */
  border-radius: 20px;
  background-color: #ffd700; /* Gold background */
  padding: 8px; /* Padding similar to the example */
  font-family: 'Lato', 'Gill Sans', 'Calibri', sans-serif; /* Font style from the example */
  box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.6); /* Slight shadow for depth */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  background-color: transparent; /* Keep header transparent */
  color: black; /* Darker text color */
}

.card-header h2, .card-header .hp {
  font-size: 20px; /* Font size from the example */
  margin: 0;
  font-weight: bold; /* Bold text for prominence */
  background-color: rgba(255, 255, 255, 0.5); /* Slight transparency for background */
  padding: 2px 5px;
  border-radius: 5px;
}

.card-image {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
  border: 5px yellow outset; /* Outset border like the example */
  padding: 2px;
  border-radius: 10px; /* Rounded corners */
}

.card-image img {
  height: 200px; /* Adjusted to match the example */
  object-fit: cover; /* Cover to fill the frame */
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.abilities {
  display: flex;
  justify-content: space-between;
}

.ability, .attack, .defense {
  background-color: #cd853f; /* Consistent background color */
  padding: 2px;
  border-radius: 5px;
  color: #fff;
  text-align: center; /* Centered text */
  flex: 1; /* Ensure equal width and side by side layout */
}

.ability h3, .attack h3, .defense h3 {
  font-size: 16px; /* Adjusted font size to match the example */
  margin: 0;
  font-weight: bold; /* Bold like the example */
}

.ability p, .attack p, .defense p {
  margin: 5px 0;
  font-size: 16px; /* Consistent font size */
  font-weight: bold; /* Bold text */
}

.weakness, .company-info {
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
}

.company-info {
  font-size: 14px; /* Slightly smaller font for company info */
}
</style>
