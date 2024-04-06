<script lang="ts">
  export let imageSrc: string;
  export let health: number;
  export let attack: number;
  export let defense: number;
  export let growth: number;
</script>

<div class="relative w-64 h-96 rounded-lg shadow-lg overflow-hidden">
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
</div>
