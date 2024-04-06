<script lang="ts">
  import type { PageServerData } from "./$types";
  import Card from "../Card.svelte";
  import { slide } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  export let data: PageServerData;

  let gameState = data.gameState;

  function playCard(cardName: string) {
      const cardIndex = gameState.you.hand.findIndex(name => name === cardName);
      if (cardIndex !== -1) {
          const card = data.cards.find(card => card.name === cardName);
          gameState.you.hand.splice(cardIndex, 1);
          gameState.you.inPlay.push({ name: cardName, health: card?.health || 0 });
          gameState = gameState;
      }
  }
</script>

<div class="game-container bg-gradient-to-b from-amber-400 to-rose-600 text-white font-retro min-h-screen">
  <div class="health-bars container mx-auto px-4 py-6 flex justify-between items-center">
    <div class="health-bar text-2xl">Your Health: {gameState.you.health}</div>
    <div class="health-bar text-2xl">Opponent's Health: {gameState.opponent.health}</div>
  </div>

  <div class="opponent-play-area container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold mb-4">Opponent's Play Area</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each gameState.opponent.inPlay as card, i (card.name)}
        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
          <Card
            name={card.name}
            health={card.health}
            defense={data.cards.find(({name}) => card.name === name)?.defense || 0}
            attack={data.cards.find(({name}) => card.name === name)?.attack || 0}
            growth={data.cards.find(({name}) => card.name === name)?.growth || 0}
            image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
          />
        </div>
      {/each}
    </div>
  </div>

  <div class="your-play-area container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold mb-4">Your Play Area</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each gameState.you.inPlay as card, i (card.name)}
        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
          <Card
            name={card.name}
            health={card.health}
            defense={0}
            attack={0}
            growth={0}
            image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
          />
        </div>
      {/each}
    </div>
  </div>

  <div class="your-hand container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold mb-4">Your Hand</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each gameState.you.hand as cardName, i (cardName)}
        <div class="card-slot cursor-pointer" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
          <Card
            name={cardName}
            health={data.cards.find(card => card.name === cardName)?.health || 0}
            defense={data.cards.find(card => card.name === cardName)?.defense || 0}
            attack={data.cards.find(card => card.name === cardName)?.attack || 0}
            growth={data.cards.find(card => card.name === cardName)?.growth || 0}
            image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
            on:click={() => {
                console.log('I got called');
                playCard(cardName);
            }}
          />
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

  :global(body) {
    font-family: 'Press Start 2P', cursive;
  }

  .card-slot {
    transition: transform 0.3s ease;
  }

  .card-slot:hover {
    transform: scale(1.05);
  }
</style>
