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
    import type { PageServerData } from "./$types";
    import Card from "../Card.svelte";
    export let data: PageServerData;
</script>

<div class="flex flex-wrap gap-4">
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
