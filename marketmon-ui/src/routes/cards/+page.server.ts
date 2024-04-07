import type {PageServerLoad} from './$types';
import type {Card} from '$lib/game-types';


export const load: PageServerLoad = async ({fetch}) => {
    const response = await fetch('/data.json');
    const cards: Card[] = await response.json();

    return {
        cards
    };
}
