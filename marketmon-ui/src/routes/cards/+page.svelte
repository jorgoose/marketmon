<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
  import Navbar from "../Navbar.svelte";

export let data: PageServerData;

</script>
    
<div
    class="min-h-screen bg-gradient-to-b from-blue-600 to-blue-500 text-white font-poppins"
  >
    <Navbar/>

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
                        company={card.name}
                        ticker={card.ticker}
                        sector={card.sector}
                    />
            {/each}
        </div>
    </div>
</div>
