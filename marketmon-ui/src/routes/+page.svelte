<script>
    import Card from "./Card.svelte";
</script>
<div class="min-h-screen bg-gradient-to-b from-amber-400 to-rose-600 text-white font-retro">
    <header class="container mx-auto px-4 py-6 flex justify-between items-center">
        <h1 class="text-4xl font-bold tracking-wide">Marketmon</h1>
        <nav class="hidden md:block">
            <ul class="flex space-x-6">
                <li><a href="/" class="hover:text-yellow-200">Home</a></li>
                <li><a href="/about" class="hover:text-yellow-200">About</a></li>
                <li><a href="/cards" class="hover:text-yellow-200">Cards</a></li>
                <li><a href="/play" class="hover:text-yellow-200">Play</a></li>
            </ul>
        </nav>
    </header>

    <main class="container mx-auto px-4 py-12">
        <section class="text-center">
            <h2 class="text-5xl font-bold mb-4">Welcome to Marketmon!</h2>
            <p class="text-xl mb-8">Collect, trade, and battle with cards based on S&P 500 companies.</p>
            <a href="/play" class="inline-block bg-yellow-400 text-black font-bold py-4 px-8 rounded-full shadow-lg hover:bg-yellow-500 transition duration-300">Start Playing</a>
        </section>

        <section class="mt-20">
            <h3 class="text-3xl font-bold mb-4">Real-Time Market Dynamics</h3>
            <p class="text-lg mb-8">Marketmon cards update dynamically to reflect current market conditions, providing a unique and engaging gaming experience.</p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <Card
                    name={'Terraformer'}
                    health={10}
                    growth={11}
                    attack={3}
                    defense={1}
                    sector={'Industrials'}
                    company={'Caterpillar Inc.'}
                    ticker={'CAT'}
                    image={'/terraformer.png'}
                />
                <Card
                    name={'Terraktor'}
                    health={8}
                    growth={12}
                    attack={2}
                    defense={2}
                    sector={'Industrials'}
                    company={'John Deere'}
                    ticker={'DE'}
                    image={'/terraktor.png'}
                    color={"#00c04b"}
                />
            </div>
        </section>
    </main>

    <footer class="container mx-auto px-4 py-6 text-center">
        <p>&copy; 2024 Marketmon. All rights reserved.</p>
    </footer>
</div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

:global(body) {
    font-family: 'Press Start 2P', cursive;
}
</style>
