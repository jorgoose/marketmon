import type {RequestHandler} from './$types';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({request}) => {
    const {gameState, action}: {
        gameState: GameState,
        action: Action
    } = await request.json();

    if (action.actionType === 'play') {
        const hand = [...gameState[gameState.whosTurn].hand];
        const inPlay = [...gameState[gameState.whosTurn].inPlay];
        const health = gameState[gameState.whosTurn].health;
        const cardIndex = hand.findIndex(n => n === action.data as string)
        const response = await fetch('/data.json');
        const cards: Card[] = await response.json();
        const card = cards.find(card => card.name === action.data as string);

        fetch('/')

        hand.splice(cardIndex, 1);
        inPlay.push({
            name: action.data as string,
            health: card?.health || 0
        })

        const newGameState: GameState = {
            ...gameState,
            [gameState.whosTurn]: {
                hand,
                inPlay,
                health: health - (card?.health || 0)
            }
        }

        return json({
            ...newGameState
        })
    }

    return json({chris: 'chris'});
}
