import type {PageServerLoad} from './$types';
import type {Card, Player, GameState} from '../../lib/game-types';

function generateRandomNumbers(n: number, k: number) {
    if (n > k + 1) {
        throw new Error("n cannot be greater than k + 1");
    }

    const numbers = Array.from({ length: k + 1 }, (_, index) => index);
    const result = [];

    for (let i = 0; i < n; i++) {
        const randomIndex = Math.floor(Math.random() * numbers.length);
        result.push(numbers[randomIndex]);
        numbers.splice(randomIndex, 1);
    }

    return result;
}

export const load: PageServerLoad = async ({fetch}) => {
    const response = await fetch('/data.json');
    const cards: Card[] = await response.json();

    const youIndexes = generateRandomNumbers(8, cards.length);
    const opponentIndexes = generateRandomNumbers(8, cards.length);

    const generatePlayer = (ar: number[]): Player => ({
        hand: ar.map(i => cards[i].name),
        inPlay: [],
        health: 100
    });

    const gameState: GameState = {
        you: generatePlayer(youIndexes),
        opponent: generatePlayer(opponentIndexes),
        whosTurn: 'you'
    }

    return {
        cards,
        gameState
    };
}
