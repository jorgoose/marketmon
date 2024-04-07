<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";

export let data: PageServerData;

</script>
    
<div
    class="min-h-screen bg-gradient-to-b from-blue-900 to-blue-500 text-white font-poppins"
  >
    <header
      class="container mx-auto px-4 py-6 flex justify-between items-center shadow-md"
    >
      <h1 class="text-4xl font-bold tracking-wide">Marketmon</h1>
      <nav class="hidden md:block">
        <ul class="flex space-x-6">
          <li>
            <a href="/" class="hover:text-blue-200 transition duration-300">Home</a>
          </li>
          <li>
            <a href="/about" class="hover:text-blue-200 transition duration-300"
              >About</a
            >
          </li>
          <li>
            <a href="/cards" class="hover:text-blue-200 transition duration-300"
              >Cards</a
            >
          </li>
          <li>
            <a href="/play" class="hover:text-blue-200 transition duration-300"
              >Play</a
            >
          </li>
        </ul>
      </nav>
    </header>
  

    <div class="your-hand container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-8">
            {#each data.cards as card}
                    <Card
                        sizeMultiplier={.9}
                        name={card.name}
                        health={card.health || 0}
                        defense={card.defense || 0}
                        attack={card.attack || 0}
                        growth={card.growth || 0}
                        image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                        company={'chris is dumb'}
                        ticker={'chris is dumb'}
                        sector={'chris is dumb'}
                    />
            {/each}
        </div>
    </div>
</div>

<style>


.card-slot {
    transition: transform 0.3s ease;
}

.card-slot:hover {
    transform: scale(1.05);
}
</style>
