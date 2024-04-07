<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
import { slide } from 'svelte/transition';
import { quintOut } from 'svelte/easing';
import type {GameState, Action, Attack, Card as CardT} from '$lib/game-types';

export let data: PageServerData;

let gameState = data.gameState;
let selectedCard: string | null = null;

function getOpponentValidActions(gameState: GameState, cards: CardT[]): Action[] {
    const { hand, inPlay, health } = gameState.opponent;
    const opponentInPlay = gameState.you.inPlay;

    return hand.reduce((validActions, cardTicker) => {
        const cost = cards.find(({ ticker }) => ticker === cardTicker)?.health || 0;
        if (cost <= health) {
            validActions.push({
                actionType: 'play',
                data: cardTicker,
            });
        }
        return validActions;
    }, [] as Action[]).concat(
            inPlay.reduce((validActions, card) => {
                validActions.push({
                    actionType: 'grow',
                    data: card.ticker,
                });
                return validActions;
            }, [] as Action[]),
            inPlay.reduce((validActions, attackerCard) => {
                return validActions.concat(
                    opponentInPlay.map((opponentCard) => ({
                        actionType: 'attack',
                        data: {
                            attacker: attackerCard.ticker,
                            opponent: opponentCard.ticker,
                        },
                    }))
                );
            }, [] as Action[])
        );
}

const updateGameState = (stateOfGame: GameState, action: Action, cards: CardT[]): GameState => {
    const state = computeNewState(stateOfGame, action, cards);
    const moves = getOpponentValidActions(state, cards);
    const move = moves[Math.floor(Math.random() * moves.length)];
    const thing = computeNewState(state, move, cards);

    return thing;
};

const computeNewState = (gameState: GameState, action: Action, cards: CardT[]): GameState => {
    const { whosTurn } = gameState;
    const notWhosTurn = whosTurn === 'you' ? 'opponent' : 'you';
    const { hand, inPlay, health } = gameState[whosTurn];

    if (action.actionType === 'play') {
        const cardIndex = hand.indexOf(action.data as string);
        const cardHealth = cards.find(({ ticker }) => ticker === action.data)?.health || 0;
        return {
            ...gameState,
            [whosTurn]: {
                inPlay: [...inPlay, { ticker: action.data as string, health: cardHealth }],
                hand: hand.filter((_, i) => i !== cardIndex),
                health: health - cardHealth,
            },
            whosTurn: notWhosTurn,
        };
    } else if (action.actionType === 'grow') {
        const growth = cards.find(({ ticker }) => ticker === action.data)?.growth || 0;
        return {
            ...gameState,
            [whosTurn]: {
                ...gameState[whosTurn],
                health: health + growth,
            },
            whosTurn: notWhosTurn,
        };
    } else {
        const { inPlay: opInPlay } = gameState[notWhosTurn];
        const actionAttack = action.data as Attack;
        const { attack } = cards.find(({ ticker }) => ticker === actionAttack.attacker)!;
        const { defense } = cards.find(({ ticker }) => ticker === actionAttack.opponent)!;
        const cardIndex = opInPlay.findIndex(({ ticker }) => ticker === actionAttack.opponent);
        const opponentHealth = opInPlay[cardIndex].health - Math.max(attack - defense, 0);
        return {
            ...gameState,
            [notWhosTurn]: {
                ...gameState[notWhosTurn],
                inPlay: opInPlay.filter((_, i) => i !== cardIndex).concat(
                    opponentHealth <= 0 ? [] : [{ ...opInPlay[cardIndex], health: opponentHealth }]
                ),
            },
            whosTurn: notWhosTurn,
        };
    }
};

function playCard(cardTicker: string) {
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
        <div class="health-bars container mx-auto px-4 py-6 flex justify-between items-center">
        <div class="health-bar text-2xl">Your Health: {gameState.you.health}</div>
        <div class="health-bar text-2xl">Opponent's Health: {gameState.opponent.health}</div>
    </div>

    <div class="opponent-play-area container mx-auto px-4 py-8">
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
                    />
                </div>
            {/each}
        </div>
    </div>

    <div class="your-play-area container mx-auto px-4 py-8">
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
                    />
                    {#if selectedCard === card.ticker}
                        <div class="actions">
                            <button on:click={() => growCard(card.ticker)}>Grow</button>
                            {#each gameState.opponent.inPlay as opponentCard (opponentCard.ticker)}
                                <button on:click={() => attackCard(card.ticker, opponentCard.ticker)}>
                                    Attack {data.cards.find(c => c.ticker === opponentCard.ticker)?.name || opponentCard.ticker}
                                </button>
                            {/each}
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    </div>

    <div class="your-hand container mx-auto px-4 py-8">
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
