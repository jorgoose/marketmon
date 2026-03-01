import type { GameState, Action, Card, Attack, GameUpdate } from '$lib/game-types';

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
    'Consumer Cyclical': 'Basic Materials',
    'Basic Materials': 'Technology',
};

const WEAKNESS_MULTIPLIER = 2;

function isSuperEffective(attackerSector: string, defenderSector: string): boolean {
    return WEAKNESS_MAP[attackerSector] === defenderSector;
}

function getValidActions(gameState: GameState, cards: Card[], player: 'you' | 'opponent'): Action[] {
    const { hand, inPlay, health } = gameState[player];
    const opponentPlayer = player === 'you' ? 'opponent' : 'you';
    const opponentInPlay = gameState[opponentPlayer].inPlay;
    const actions: Action[] = [];

    // Deploy actions — cost is ceil(HP/2), must keep at least 1 HP
    for (const cardTicker of hand) {
        const card = cards.find(({ ticker }) => ticker === cardTicker);
        if (!card) continue;
        const cost = Math.ceil(card.health / 2);
        if (cost < health) {
            actions.push({ actionType: 'play', data: cardTicker });
        }
    }

    // Grow actions — always valid for any card in play
    for (const card of inPlay) {
        actions.push({ actionType: 'grow', data: card.ticker });
    }

    if (opponentInPlay.length > 0) {
        // Creature-vs-creature attack actions
        for (const attacker of inPlay) {
            for (const defender of opponentInPlay) {
                actions.push({
                    actionType: 'attack',
                    data: { attacker: attacker.ticker, opponent: defender.ticker },
                });
            }
        }
    } else {
        // Face attack actions — when opponent has no creatures
        for (const attacker of inPlay) {
            actions.push({ actionType: 'attack-face', data: attacker.ticker });
        }
    }

    return actions;
}

const computeNewState = (gameState: GameState, action: Action, cards: Card[]): GameState => {
    const { whosTurn } = gameState;
    const notWhosTurn = whosTurn === 'you' ? 'opponent' : 'you';
    const { hand, inPlay, health } = gameState[whosTurn];

    if (action.actionType === 'play') {
        const cardIndex = hand.indexOf(action.data as string);
        const cardDef = cards.find(({ ticker }) => ticker === action.data);
        const cardHealth = cardDef?.health || 0;
        const cost = Math.ceil(cardHealth / 2);
        return {
            ...gameState,
            [whosTurn]: {
                inPlay: [...inPlay, { ticker: action.data as string, health: cardHealth }],
                hand: hand.filter((_, i) => i !== cardIndex),
                health: health - cost,
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
    } else if (action.actionType === 'attack') {
        // Mutual combat
        const { inPlay: opInPlay } = gameState[notWhosTurn];
        const actionAttack = action.data as Attack;
        const attackerCard = cards.find(({ ticker }) => ticker === actionAttack.attacker)!;
        const defenderCard = cards.find(({ ticker }) => ticker === actionAttack.opponent)!;

        // Damage to defender
        const baseDamage = Math.max(attackerCard.attack - defenderCard.defense, 1);
        const multiplier = isSuperEffective(attackerCard.sector, defenderCard.sector) ? WEAKNESS_MULTIPLIER : 1;
        const damage = Math.floor(baseDamage * multiplier);

        // Counter-damage to attacker (no super effective)
        const baseCounter = Math.max(defenderCard.attack - attackerCard.defense, 1);
        const counterDamage = baseCounter;

        const defenderIndex = opInPlay.findIndex(({ ticker }) => ticker === actionAttack.opponent);
        const attackerIndex = inPlay.findIndex(({ ticker }) => ticker === actionAttack.attacker);
        const defenderHp = opInPlay[defenderIndex].health - damage;
        const attackerHp = inPlay[attackerIndex].health - counterDamage;

        return {
            ...gameState,
            [whosTurn]: {
                ...gameState[whosTurn],
                inPlay: inPlay
                    .map((card, i) => i === attackerIndex ? { ...card, health: attackerHp } : card)
                    .filter((card) => card.health > 0),
            },
            [notWhosTurn]: {
                ...gameState[notWhosTurn],
                inPlay: opInPlay
                    .map((card, i) => i === defenderIndex ? { ...card, health: defenderHp } : card)
                    .filter((card) => card.health > 0),
            },
            whosTurn: notWhosTurn,
        };
    } else {
        // attack-face: direct damage to opponent player HP
        const attackerTicker = action.data as string;
        const attackerCard = cards.find(({ ticker }) => ticker === attackerTicker)!;
        const damage = attackerCard.attack;
        return {
            ...gameState,
            [notWhosTurn]: {
                ...gameState[notWhosTurn],
                health: gameState[notWhosTurn].health - damage,
            },
            whosTurn: notWhosTurn,
        };
    }
};

function selectBotAction(gameState: GameState, cards: Card[]): Action | null {
    const actions = getValidActions(gameState, cards, 'opponent');
    if (actions.length === 0) return null;

    const deployActions = actions.filter((a) => a.actionType === 'play');
    const attackActions = actions.filter((a) => a.actionType === 'attack');
    const faceActions = actions.filter((a) => a.actionType === 'attack-face');
    const growActions = actions.filter((a) => a.actionType === 'grow');

    const opInPlay = gameState.opponent.inPlay;
    const playerHp = gameState.you.health;

    // Helper: get card def by ticker
    const cardDef = (ticker: string) => cards.find((c) => c.ticker === ticker)!;

    // Helper: get best deploy by ATK
    const bestDeploy = () => {
        if (deployActions.length === 0) return null;
        return deployActions.reduce((best, a) => {
            const atkA = cardDef(a.data as string).attack;
            const atkB = cardDef(best.data as string).attack;
            return atkA > atkB ? a : best;
        });
    };

    // 1. Field empty + can deploy → highest ATK affordable card
    if (opInPlay.length === 0 && deployActions.length > 0) {
        return bestDeploy()!;
    }

    // 2. Can face attack + player HP ≤ 20 → highest ATK creature goes face
    if (faceActions.length > 0 && playerHp <= 20) {
        return faceActions.reduce((best, a) => {
            const atkA = cardDef(a.data as string).attack;
            const atkB = cardDef(best.data as string).attack;
            return atkA > atkB ? a : best;
        });
    }

    // 3. Super-effective attack available → highest damage one
    const seAttacks = attackActions.filter((a) => {
        const atk = a.data as Attack;
        return isSuperEffective(cardDef(atk.attacker).sector, cardDef(atk.opponent).sector);
    });
    if (seAttacks.length > 0) {
        return seAttacks.reduce((best, a) => {
            const atkData = a.data as Attack;
            const bestData = best.data as Attack;
            const dmgA = Math.floor(Math.max(cardDef(atkData.attacker).attack - cardDef(atkData.opponent).defense, 1) * WEAKNESS_MULTIPLIER);
            const dmgB = Math.floor(Math.max(cardDef(bestData.attacker).attack - cardDef(bestData.opponent).defense, 1) * WEAKNESS_MULTIPLIER);
            return dmgA > dmgB ? a : best;
        });
    }

    // 4. Can kill enemy creature AND survive counter → take the kill
    const killAttacks = attackActions.filter((a) => {
        const atk = a.data as Attack;
        const attackerDef = cardDef(atk.attacker);
        const defenderDef = cardDef(atk.opponent);
        const defenderInPlay = gameState.you.inPlay.find((c) => c.ticker === atk.opponent);
        const attackerInPlay = opInPlay.find((c) => c.ticker === atk.attacker);
        if (!defenderInPlay || !attackerInPlay) return false;
        const dmg = Math.max(attackerDef.attack - defenderDef.defense, 1);
        const counter = Math.max(defenderDef.attack - attackerDef.defense, 1);
        return dmg >= defenderInPlay.health && attackerInPlay.health > counter;
    });
    if (killAttacks.length > 0) {
        return killAttacks[0];
    }

    // 5. Own creature < 40% HP and growth ≥ 4 → grow it
    const healCandidates = growActions.filter((a) => {
        const ticker = a.data as string;
        const def = cardDef(ticker);
        const inPlayCard = opInPlay.find((c) => c.ticker === ticker);
        if (!inPlayCard) return false;
        return inPlayCard.health < def.health * 0.4 && def.growth >= 4;
    });
    if (healCandidates.length > 0) {
        return healCandidates[0];
    }

    // 6. Can face attack → go face (highest ATK)
    if (faceActions.length > 0) {
        return faceActions.reduce((best, a) => {
            const atkA = cardDef(a.data as string).attack;
            const atkB = cardDef(best.data as string).attack;
            return atkA > atkB ? a : best;
        });
    }

    // 7. Can attack creatures → best damage-to-counter ratio
    if (attackActions.length > 0) {
        return attackActions.reduce((best, a) => {
            const atkData = a.data as Attack;
            const bestData = best.data as Attack;
            const dmgA = Math.max(cardDef(atkData.attacker).attack - cardDef(atkData.opponent).defense, 1);
            const counterA = Math.max(cardDef(atkData.opponent).attack - cardDef(atkData.attacker).defense, 1);
            const dmgB = Math.max(cardDef(bestData.attacker).attack - cardDef(bestData.opponent).defense, 1);
            const counterB = Math.max(cardDef(bestData.opponent).attack - cardDef(bestData.attacker).defense, 1);
            const ratioA = dmgA / Math.max(counterA, 1);
            const ratioB = dmgB / Math.max(counterB, 1);
            return ratioA > ratioB ? a : best;
        });
    }

    // 8. Can deploy → highest ATK card
    if (deployActions.length > 0) {
        return bestDeploy()!;
    }

    // 9. Fallback → grow anything
    if (growActions.length > 0) {
        return growActions[0];
    }

    return actions[0] || null;
}

export { isSuperEffective };

export const updateGameState = (stateOfGame: GameState, action: Action, cards: Card[]): GameUpdate => {
    if (stateOfGame.winner) {
        return { state: stateOfGame };
    }

    // 1. Apply player's action
    let state = computeNewState(stateOfGame, action, cards);

    // 2. Check opponent HP ≤ 0 → player wins
    if (state.opponent.health <= 0) {
        return { state: { ...state, winner: 'you' } };
    }

    // 3. Bot turn loop
    let firstBotAction: Action | undefined;
    for (let i = 0; i < 20; i++) {
        const botAction = selectBotAction(state, cards);
        if (!botAction) {
            // Bot has no moves — check if it's a stalemate or skip
            break;
        }
        if (!firstBotAction) {
            firstBotAction = botAction;
        }

        // Apply bot action
        state = computeNewState(state, botAction, cards);

        // Check player HP ≤ 0 → opponent wins
        if (state.you.health <= 0) {
            return { state: { ...state, winner: 'opponent' }, botAction: firstBotAction };
        }

        // Check if player has valid moves → if yes, break loop
        const playerMoves = getValidActions(state, cards, 'you');
        if (playerMoves.length > 0) {
            break;
        }

        // Player can't act — flip whosTurn back to opponent, loop again
        state = { ...state, whosTurn: 'opponent' };
    }

    return { state, botAction: firstBotAction };
};
