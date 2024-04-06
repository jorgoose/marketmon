<script lang="ts">
  export let imageSrc: string;
  export let health: number;
  export let attack: number;
  export let defense: number;
  export let growth: number;

  let isHovered = false;
  let particleCount = 10;
</script>

<div
  class="relative w-64 h-96 rounded-lg shadow-lg overflow-hidden transition-transform duration-500 ease-out transform hover:scale-105 hover:rotate-2 hover:shadow-2xl"
  on:mouseenter={() => (isHovered = true)}
  on:mouseleave={() => (isHovered = false)}
>
  <img class="w-full h-full object-cover" src={imageSrc} alt="Pokémon Card" />
  <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4 text-white">
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm">Health</span>
      <span class="text-xl font-bold">{health}</span>
    </div>
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm">Attack</span>
      <span class="text-xl font-bold">{attack}</span>
    </div>
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm">Defense</span>
      <span class="text-xl font-bold">{defense}</span>
    </div>
    <div class="flex justify-between items-center">
      <span class="text-sm">Growth</span>
      <span class="text-xl font-bold">{growth}</span>
    </div>
  </div>

  {#if isHovered}
    <div class="absolute inset-0 pointer-events-none">
      {#each Array(particleCount) as _, i}
        <div
          class="absolute rounded-full bg-white opacity-0 animate-particle"
          style="left: {Math.random() * 100}%; top: {Math.random() * 100}%; width: {Math.random() * 3 + 2}px; height: {Math.random() * 3 + 2}px; animation-duration: {Math.random() + 0.5}s; animation-delay: {i * 0.1}s;"
        ></div>
      {/each}
    </div>
  {/if}
</div>

<style>
  @keyframes particle {
    0% {
      opacity: 0;
      transform: translate(0, 0);
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0;
      transform: translate(0, -20px);
    }
  }

  .animate-particle {
    animation-name: particle;
    animation-iteration-count: infinite;
    animation-timing-function: linear;
  }
</style>
