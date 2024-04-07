<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
import { slide } from 'svelte/transition';
import { quintOut } from 'svelte/easing';
import type {GameState, Action, Attack, Card as CardT} from '../../lib/game-types';

export let data: PageServerData;

let gameState = data.gameState;

const updateGameState = (gameState: GameState, action: Action, cards: CardT[]): GameState => {
    const {whosTurn} = gameState;
    const notWhosTurn = whosTurn === 'you' ? 'opponent' : 'you';
    const {hand, inPlay, health} = gameState[whosTurn];

    if (action.actionType === 'play') {
        const cardIndex = hand.indexOf(action.data as string);

        const cardHealth = cards.find(({name}) => name === action.data)?.health || 0;

        hand.splice(cardIndex, 1);
        inPlay.push({
            name: action.data as string,
            health: cardHealth
        });

        return {
            ...gameState,
            [whosTurn]: {
                inPlay,
                hand,
                health: health - cardHealth
            },
            whosTurn: notWhosTurn
        }
    } else if (action.actionType === 'grow') {
        const growth = cards.find(({name}) => name === action.data)?.growth || 0;

        return {
            ...gameState,
            [whosTurn]: {
                ...gameState[whosTurn],
                health: health + growth
            },
            whosTurn: notWhosTurn
        }
    } else {
        const {inPlay: opInPlay} = gameState[notWhosTurn];
        const actionAttack = action.data as Attack;
        const {attack} = cards.find(({name}) => name === actionAttack.attacker)!;
        const {defense} = cards.find(({name}) => name === actionAttack.opponent)!;
        const cardIndex = opInPlay.findIndex(({name}) => name === actionAttack.opponent);
        let {health: opponentHealth} = opInPlay[cardIndex];
        opponentHealth -= attack + defense; // should this be a scaling factor?

        if (opponentHealth <= 0) {
            opInPlay.splice(cardIndex, 1);
        } else {
            opInPlay[cardIndex].health = opponentHealth;
        }

        return {
            ...gameState,
            [notWhosTurn]: {
                ...gameState[notWhosTurn],
                inPlay: opInPlay
            },
            whosTurn: notWhosTurn
        }
    }
}

async function playCard(cardName: string) {
    const action: Action = {
        actionType: 'play',
        data: cardName
    };

    console.log(gameState);
    gameState = updateGameState(gameState, action, data.cards);
    console.log(gameState);
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
                        sizeMultiplier={0.5}
                        image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                        name={card.name}
                        health={card.health}
                        defense={data.cards.find(({name}) => card.name === name)?.defense || 0}
                        attack={data.cards.find(({name}) => card.name === name)?.attack || 0}
                        growth={data.cards.find(({name}) => card.name === name)?.growth || 0}
                        company={card.name}
                        ticker={card.name}
                        sector={card.name}
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
                        sizeMultiplier={0.5}
                        name={card.name}
                        health={card.health}
                        defense={data.cards.find(card => card.name === card.name)?.defense || 0}
                        attack={data.cards.find(card => card.name === card.name)?.attack || 0}
                        growth={data.cards.find(card => card.name === card.name)?.growth || 0}
                        image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                        company={card.name}
                        ticker={card.name}
                        sector={card.name}
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
                        sizeMultiplier={0.5}
                        name={cardName}
                        health={data.cards.find(card => card.name === cardName)?.health || 0}
                        defense={data.cards.find(card => card.name === cardName)?.defense || 0}
                        attack={data.cards.find(card => card.name === cardName)?.attack || 0}
                        growth={data.cards.find(card => card.name === cardName)?.growth || 0}
                        image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                        on:click={() => {
                            playCard(cardName);
                        }}
                        company={cardName}
                        ticker={cardName}
                        sector={cardName}
                    />
                </div>
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
