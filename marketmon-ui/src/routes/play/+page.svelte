<script lang='ts' context='module'>
type Player = {
  hand: string[],
  inPlay: {
    name: string;
    health: number;
  }[];
  health: number;
};

type Action = {
  actionType: 'play' | 'attack' | 'grow',
  data: string | {
    attacker: string;
    opponent: string;
  }
};

type GameState = {
  you: Player;
  opponent: Player;
  whosTurn: 'you' | 'opponent';
};
</script>

<script lang="ts">
import {slide} from 'svelte/transition';
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
export let data: PageServerData;

let showDrawer = false;

function toggleDrawer() {
  showDrawer = !showDrawer;
}
</script>

<div class="relative h-screen overflow-hidden bg-gradient-to-r from-red-500 to-blue-500">
  <button class="absolute top-4 left-4 px-4 py-2 text-lg bg-red-600 text-white rounded cursor-pointer z-10" on:click={toggleDrawer}>
    Show Cards
  </button>
  
  {#if showDrawer}
  <div class="fixed top-0 left-0 w-96 h-full bg-white bg-opacity-90 p-4 shadow-lg overflow-y-auto z-20" transition:slide={{ duration: 300 }}>
    <div class="grid grid-cols-2 gap-4">
      {#each data.cards as card}
      <Card
        name={card.name}
        health={card.health}
        defense={card.defense}
        attack={card.attack}
        growth={card.growth}
        image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
      />
      {/each}
    </div>
  </div>
  {/if}
  
  <div class="absolute inset-0 flex">
    <div class="w-1/2 bg-blue-100"></div>
    <div class="w-1/2 bg-red-100"></div>
    <div class="absolute inset-y-0 left-1/2 transform -translate-x-1/2 w-1 bg-white"></div>
  </div>
</div>
