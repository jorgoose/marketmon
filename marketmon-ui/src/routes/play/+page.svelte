<script lang="ts">
    import type { PageData } from "./$types";
    import Card from "../Card.svelte";

    export let data: PageData;
</script>

<div class='card-container'>
    {#each Object.entries(data.data) as card}
        <Card
            name={card[0]}
            health={card[1].health}
            defense={card[1].defense}
            attack={card[1].attack}
            growth={card[1].growth}
            image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
        />
    {/each}
</div>

<style>
  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
</style>
