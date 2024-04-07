<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
import { slide } from 'svelte/transition';
import { quintOut } from 'svelte/easing';
import type {Action} from '$lib/game-types';
import {updateGameState} from './update-game-state';

export let data: PageServerData;

let gameState = data.gameState;
let selectedCard: string | null = null;
let showHand = false;


function playCard(cardTicker: string) {
    const health = data.cards.find(({ticker}) => ticker === cardTicker)?.health || 0;
    
    if (health > gameState.you.health) {
        alert('Not enough health to play this card');
        return;
    }

    const action: Action = {
        actionType: 'play',
        data: cardTicker
    };

    gameState = updateGameState(gameState, action, data.cards);
}

function growCard(cardTicker: string) {
    const action: Action = {
        actionType: 'grow',
        data: cardTicker
    };

    gameState = updateGameState(gameState, action, data.cards);
}

function attackCard(attackerTicker: string, opponentTicker: string) {
    const action: Action = {
        actionType: 'attack',
        data: {
            attacker: attackerTicker,
            opponent: opponentTicker
        }
    };

    gameState = updateGameState(gameState, action, data.cards);
    selectedCard = null;
}
</script>

<div class="min-h-screen bg-gradient-to-b from-blue-700 to-blue-500 text-white font-poppins">
    <div class="game-container">
        <div class="opponent-side">
            <div class="health-bar text-2xl">Opponent's Health: {gameState.opponent.health}</div>
            <div class="opponent-play-area">
                <h2 class="text-3xl font-bold mb-4">Opponent's Play Area</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {#each gameState.opponent.inPlay as card, i (card.ticker)}
                        {@const cardData = data.cards.find(({ticker}) => ticker === card.ticker)}
                        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                            <Card
                                image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                                name={cardData?.name || ''}
                                health={card.health}
                                defense={cardData?.defense || 0}
                                attack={cardData?.attack || 0}
                                growth={cardData?.growth || 0}
                                company={cardData?.name || ''}
                                ticker={card.ticker}
                                sector={cardData?.sector || ''}
                                sizeMultiplier={0.8}
                            />
                        </div>
                    {/each}
                </div>
            </div>
        </div>
        <div class="your-side">
            <div class="health-bar text-2xl">Your Health: {gameState.you.health}</div>
            <div class="your-play-area">
                <h2 class="text-3xl font-bold mb-4">Your Play Area</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {#each gameState.you.inPlay as card, i (card.ticker)}
                        {@const cardData = data.cards.find(c => c.ticker === card.ticker)}
                        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                            <Card
                                name={cardData?.name || ''}
                                health={card.health}
                                defense={cardData?.defense || 0}
                                attack={cardData?.attack || 0}
                                growth={cardData?.growth || 0}
                                image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                                company={cardData?.name || ''}
                                ticker={card.ticker}
                                sector={cardData?.sector || ''}
                                on:click={() => {
                                    if (selectedCard === card.ticker) {
                                        selectedCard = null;
                                    } else if (!selectedCard) {
                                        selectedCard = card.ticker;
                                    }
                                }}
                                color={selectedCard === card.ticker ? 'lightblue' : ''}
                                sizeMultiplier={0.8}
                            />
                        </div>
                    {/each}
                </div>
            </div>
            <button class="hand-button" on:click={() => showHand = !showHand}>
                {showHand ? 'Hide Hand' : 'Show Hand'}
            </button>
            {#if showHand}
                <div class="your-hand" transition:slide|local={{ duration: 500, easing: quintOut }}>
                    <h2 class="text-3xl font-bold mb-4">Your Hand</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {#each gameState.you.hand as cardTicker, i (cardTicker)}
                            {@const cardData = data.cards.find(card => card.ticker === cardTicker)}
                            <div class="card-slot cursor-pointer" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                                <Card
                                    name={cardData?.name || ''}
                                    health={cardData?.health || 0}
                                    defense={cardData?.defense || 0}
                                    attack={cardData?.attack || 0}
                                    growth={cardData?.growth || 0}
                                    image={'https://img.pokemondb.net/sprites/scarlet-violet/normal/charizard.png'}
                                    on:click={() => {
                                        if (gameState.whosTurn === 'you') {
                                            playCard(cardTicker);
                                        }
                                    }}
                                    company={cardData?.name || ''}
                                    ticker={cardTicker}
                                    sector={cardData?.sector || ''}
                                    sizeMultiplier={0.8}
                                />
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        </div>
    </div>
    {#if selectedCard}
        <div class="global-actions">
            <button on:click={() => growCard(selectedCard || '')}>Grow</button>
            {#each gameState.opponent.inPlay as opponentCard (opponentCard.ticker)}
                <button on:click={() => attackCard(selectedCard || '', opponentCard.ticker)}>
                    Attack {data.cards.find(c => c.ticker === opponentCard.ticker)?.name || opponentCard.ticker}
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
.game-container {
    display: flex;
}

.opponent-side,
.your-side {
    flex: 1;
    padding: 20px;
}

.opponent-play-area,
.your-play-area {
    margin-top: 20px;
}

.hand-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4a5568;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.your-hand {
    margin-top: 20px;
}

.global-actions {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
}

.global-actions button {
    padding: 10px 20px;
    background-color: #4a5568;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.card-slot {
    transition: transform 0.3s ease;
}

.card-slot:hover {
    transform: scale(1.05);
}
</style>
