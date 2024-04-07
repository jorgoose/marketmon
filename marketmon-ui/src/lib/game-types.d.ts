export type Card = {
    name: string
    health: number;
    attack: number;
    growth: number;
    defense: number;
}

type Player = {
  hand: string[],
  inPlay: {
    name: string;
    health: number;
  }[];
  health: number;
};

type Attack = {
    attacker: string;
    opponent: string;
};

type Action = {
  actionType: 'play' | 'attack' | 'grow',
  data: string | Attack
};

type GameState = {
  you: Player;
  opponent: Player;
  whosTurn: 'you' | 'opponent';
};
