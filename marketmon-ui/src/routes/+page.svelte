<script>
    import Card from "./Card.svelte";
    import Navbar from "./Navbar.svelte";
  </script>
  
  <div
    class="min-h-screen bg-gradient-to-b from-blue-900 to-blue-500 text-white font-poppins"
  >
    <Navbar />
    <main class="container mx-auto px-4 py-12">
      <section class="text-center">
        <h2 class="text-5xl font-bold mb-4">Welcome to Marketmon!</h2>
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
        <h3 class="text-3xl font-bold mb-4">Real-Time Market Dynamics</h3>
        <p class="text-lg mb-8">
          Marketmon cards update dynamically to reflect current market conditions,
          providing a unique and engaging gaming experience.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card
            name="Terraformer"
            health={10}
            growth={11}
            attack={3}
            defense={1}
            sector="Industrials"
            company="Caterpillar Inc."
            ticker="CAT"
            image="/terraformer.png"
          />
          <Card
            name="Terraktor"
            health={8}
            growth={12}
            attack={2}
            defense={2}
            sector="Industrials"
            company="John Deere"
            ticker="DE"
            image="/terraktor.png"
            color="#00c04b"
          />
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
  </style>