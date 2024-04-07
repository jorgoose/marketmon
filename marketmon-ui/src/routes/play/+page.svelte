<script lang="ts">
    import type { PageServerData } from "./$types";
    import Card from "../Card.svelte";
    import { slide } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
    import type { Action } from '$lib/game-types';
    import { updateGameState } from './update-game-state';
    
    export let data: PageServerData;
    
    let gameState = data.gameState;
    let selectedCard: string | null = null;
    let showHand = false;
    
    function playCard(cardTicker: string) {
        const health = data.cards.find(({ ticker }) => ticker === cardTicker)?.health || 0;
    
        if (health > gameState.you.health) {
            alert('Not enough health to play this card');
            return;
        }
    
        const action: Action = {
            actionType: 'play',
            data: cardTicker
        };
    
        gameState = updateGameState(gameState, action, data.cards);
        selectedCard = null;
    }
    
    function growCard(cardTicker: string) {
        const action: Action = {
            actionType: 'grow',
            data: cardTicker
        };
    
        gameState = updateGameState(gameState, action, data.cards);
        selectedCard = null;
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
    
    <div class="min-h-screen bg-gradient-to-b from-blue-700 to-blue-500 text-white font-poppins relative">
        {#if gameState.winner}
        <div class="modal">
            <div class="modal-content">
                {#if gameState.winner === 'you'}
                    <h2 class="text-3xl font-bold">You Win!</h2>
                {:else}
                    <h2 class="text-3xl font-bold">You Lose!</h2>
                {/if}
            </div>
        </div>
        {/if}
    
        <div class="opponent-side">
            <div class="health-bar text-2xl">Opponent's Health: {gameState.opponent.health}</div>
            <div class="opponent-play-area">
                <!-- <h2 class="text-3xl font-bold mb-4">Opponent's Play Area</h2> -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {#each gameState.opponent.inPlay as card, i (card.ticker)}
                        {@const cardData = data.cards.find(({ ticker }) => ticker === card.ticker)}
                        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                            <Card
                                name={cardData?.creatureName || ''}
                                health={card.health}
                                defense={cardData?.defense || 0}
                                attack={cardData?.attack || 0}
                                growth={cardData?.growth || 0}
                                company={cardData?.name || ''}
                                ticker={card.ticker}
                                sector={cardData?.sector || ''}
                                sizeMultiplier={1}
                            />
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    
        <div class="your-side">
            <div class="your-play-area">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {#each gameState.you.inPlay as card, i (card.ticker)}
                        {@const cardData = data.cards.find(c => c.ticker === card.ticker)}
                        <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                            <Card
                                name={cardData?.creatureName || ''}
                                health={card.health}
                                defense={cardData?.defense || 0}
                                attack={cardData?.attack || 0}
                                growth={cardData?.growth || 0}
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
                                sizeMultiplier={1}
                            />
                        </div>
                    {/each}
                </div>
                <!-- <h2 class="text-3xl font-bold mb-4">Your Play Area</h2> -->
                <div class="health-bar text-2xl">Your Health: {gameState.you.health}</div>
            </div>
            <button class="hand-button" on:click={() => showHand = !showHand}>
                {showHand ? 'Hide Hand' : 'Show Hand'}
            </button>
            {#if showHand}
                <div class="your-hand" transition:slide|local={{ y: -200, duration: 500, easing: quintOut }}>
                    <div class="card-row">
                        {#each gameState.you.hand as cardTicker, i (cardTicker)}
                            {@const cardData = data.cards.find(card => card.ticker === cardTicker)}
                            <div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
                                <Card
                                    name={cardData?.creatureName || ''}
                                    health={cardData?.health || 0}
                                    defense={cardData?.defense || 0}
                                    attack={cardData?.attack || 0}
                                    growth={cardData?.growth || 0}
                                    on:click={() => {
                                        if (gameState.whosTurn === 'you') {
                                            playCard(cardTicker);
                                        }
                                    }}
                                    company={cardData?.name || ''}
                                    ticker={cardTicker}
                                    sector={cardData?.sector || ''}
                                    sizeMultiplier={1}
                                />
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
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
            flex-direction: column;
            justify-content: space-between;
            min-height: 100vh;
        }
    
        .opponent-side,
        .your-side {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    
        .health-bar {
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.5);
        }
    
        .opponent-side .health-bar {
            /* Algin absolute in top left */
            position: absolute;
            top: 20px;
            left: 20px;
        }
    
        .your-side .health-bar {
            /* Algin absolute in bottom right */
            position: absolute;
            bottom: 20px;
            right: 20px;
        }
    
        .opponent-play-area,
        .your-play-area {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
    
        .hand-button {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background-color: #4a5568;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    
        .your-hand {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
        }
    
        .card-row {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 10px;
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
            /* Shift children to the right */
            margin-top: 40px;
            width: 100%;
        }

    
        .card-slot:hover {
            transform: scale(1.05);
        }

        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

    .modal-content {
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    </style>