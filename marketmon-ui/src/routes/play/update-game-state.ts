import type {GameState, Action, Card, Attack} from '$lib/game-types';

const WEAKNESS_MAP: Record<string, string> = {
    'Technology': 'Communication Services',
    'Communication Services': 'Consumer Defensive',
    'Consumer Defensive': 'Healthcare',
    'Healthcare': 'Industrials',
    'Industrials': 'Energy',
    'Energy': 'Utilities',
    'Utilities': 'Real Estate',
    'Real Estate': 'Financial Services',
    'Financial Services': 'Consumer Cyclical',
    'Consumer Cyclical': 'Materials',
    'Materials': 'Technology',
};

const WEAKNESS_MULTIPLIER = 1.5;

function isSuperEffective(attackerSector: string, defenderSector: string): boolean {
    return WEAKNESS_MAP[attackerSector] === defenderSector;
}

function getValidActions(gameState: GameState, cards: Card[], player: 'you' | 'opponent'): Action[] {
    const { hand, inPlay, health } = gameState[player];
    const opponentPlayer = player === 'you' ? 'opponent' : 'you';
    const opponentInPlay = gameState[opponentPlayer].inPlay;

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

const computeNewState = (gameState: GameState, action: Action, cards: Card[]): GameState => {
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
        const cardIndex = inPlay.findIndex(({ ticker }) => ticker === action.data);
        const originalHealth = cards.find(({ ticker }) => ticker === action.data)?.health || 0;
        const currentHealth = inPlay[cardIndex].health;
        const newHealth = Math.min(currentHealth + growth, originalHealth);
        const overflowHealth = Math.max(currentHealth + growth - originalHealth, 0);
        return {
            ...gameState,
            [whosTurn]: {
                ...gameState[whosTurn],
                inPlay: inPlay.map((card, i) =>
                    i === cardIndex ? { ...card, health: newHealth } : card
                ),
                health: health + overflowHealth,
            },
            whosTurn: notWhosTurn,
        };
    } else {
        const { inPlay: opInPlay } = gameState[notWhosTurn];
        const actionAttack = action.data as Attack;
        const attackerCard = cards.find(({ ticker }) => ticker === actionAttack.attacker)!;
        const defenderCard = cards.find(({ ticker }) => ticker === actionAttack.opponent)!;
        const baseDamage = Math.max(attackerCard.attack - defenderCard.defense, 0);
        const multiplier = isSuperEffective(attackerCard.sector, defenderCard.sector) ? WEAKNESS_MULTIPLIER : 1;
        const damage = Math.floor(baseDamage * multiplier);
        const cardIndex = opInPlay.findIndex(({ ticker }) => ticker === actionAttack.opponent);
        const opponentHealth = opInPlay[cardIndex].health - damage;
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

export { isSuperEffective };

export const updateGameState = (stateOfGame: GameState, action: Action, cards: Card[]): GameState => {
    if (stateOfGame.winner) {
        return stateOfGame;
    }
    console.log(stateOfGame);
    console.log(action);
    const state = computeNewState(stateOfGame, action, cards);
    const moves = getValidActions(state, cards, 'opponent');
    if (moves.length <= 0) {
        console.log('No possible moves');
        return {
            ...state,
            winner: 'you'
        };
    }
    const move = moves[Math.floor(Math.random() * moves.length)];
    console.log(state);
    console.log(move);
    const thing = computeNewState(state, move, cards);

    if (getValidActions(thing, cards, 'you').length <= 0) {
        return {
            ...thing,
            winner: 'opponent'
        }
    }

    console.log(thing);

    return thing;
};
