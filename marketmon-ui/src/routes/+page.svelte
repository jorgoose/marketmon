<script lang="ts">
    import Card from "./Card.svelte";
    import Navbar from "./Navbar.svelte";
    import type { PageServerData } from "./$types";

    export let data: PageServerData;

    // Shuffle the cards array on page load
    let shuffledCards = shuffleArray(data.cards);

    function shuffleArray(array: any[]) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
</script>

<div
    class="min-h-screen bg-gradient-to-b from-blue-700 to-blue-500 text-white font-poppins bounding-carousel"
>
    <Navbar />
    <main class="container mx-auto px-4 py-12">
        <section class="text-center">
            <h2 class="text-5xl font-bold pt-12 pb-2">Welcome to Marketmon!</h2>
            <p class="text-xl mb-8">
                Collect, trade, and battle with cards based on S&P 500 companies.
            </p>
            <a
                href="/play"
                class="inline-block bg-blue-400 text-white font-bold py-4 px-8 rounded-full shadow-lg hover:bg-blue-500 transition duration-300"
                >Start Playing</a
            >
        </section>

        <section class="mt-20">
          <div class="ml-20">
              <h3 class="text-3xl font-bold mb-4">Real-Time Market Dynamics</h3>
              <p class="text-lg mb-8">
                  Marketmon cards update dynamically to reflect current market conditions,
                  providing a unique and engaging gaming experience.
              </p>
          </div>
          <div class="carousel-wrapper">
              <div class="carousel">
                  {#each [...shuffledCards, ...shuffledCards] as card}
                      <Card
                          sizeMultiplier={0.9}
                          name={card.creatureName}
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
      </section>
    </main>

    <footer class="container mx-auto px-4 py-6 text-center">
        <p>&copy; 2024 Marketmon. All rights reserved.</p>
    </footer>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap");
    :global(body) {
        font-family: "Poppins", sans-serif;
    }

    .bounding-carousel {
        overflow: hidden;
    }

    .carousel-wrapper {
      padding-top: 20px;
      overflow: visible;
    }

  .carousel {
      white-space: nowrap;
      display: inline-flex;
      animation: slide 900s linear infinite;
      padding: 0 20px; /* Adjust this value to control the spacing between cards */
  }

  .carousel::-webkit-scrollbar {
      display: none;
  }

  @keyframes slide {
      0% {
          transform: translateX(0);
      }
      100% {
          transform: translateX(-50%); /* Adjust this value based on the total width of the cards */
      }
  }
</style>