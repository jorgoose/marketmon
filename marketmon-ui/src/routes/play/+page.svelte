<script lang="ts">
    import type { PageData } from "./$types";
    import Card from "../Card.svelte";

    export let data: PageData;
</script>

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

<button on:click={() => {
    console.log(Object.entries(data.data)[0])
}}>
    Click me
</button>
