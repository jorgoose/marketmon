<script lang="ts">
	import type { PageServerData } from './$types';
	import Card from '../Card.svelte';
	import { fade, slide, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { Action, Attack, GameUpdate } from '$lib/game-types';
	import { updateGameState, isSuperEffective } from './update-game-state';
	import PlayerHud from './PlayerHud.svelte';
	import CardSlot from './CardSlot.svelte';
	import BattleLog from './BattleLog.svelte';

	export let data: PageServerData;

	let gameState = data.gameState;
	let selectedCard: string | null = null;
	let actionMode: 'idle' | 'select-action' | 'select-target' = 'idle';
	let battleLog: { text: string; type: string }[] = [];
	let notification = '';
	let notificationType: 'error' | 'success' = 'error';
	let notificationTimeout: ReturnType<typeof setTimeout>;
	let innerWidth: number = 1024;

	const MAX_HEALTH = 50;
	const FIELD_SLOTS = 4;

	$: fieldCardSize = innerWidth < 480 ? 0.4 : innerWidth < 768 ? 0.55 : 0.65;
	$: handCardSize = innerWidth < 480 ? 0.38 : innerWidth < 768 ? 0.5 : 0.6;

	function addLog(text: string, type: string) {
		battleLog = [...battleLog, { text, type }];
	}

	function showNotification(msg: string, type: 'error' | 'success' = 'error') {
		notification = msg;
		notificationType = type;
		clearTimeout(notificationTimeout);
		notificationTimeout = setTimeout(() => (notification = ''), 3000);
	}

	function getCreatureName(ticker: string): string {
		return data.cards.find((c) => c.ticker === ticker)?.creatureName || ticker;
	}

	function logBotAction(botAction: Action | undefined) {
		if (!botAction) return;
		if (botAction.actionType === 'play') {
			const ticker = botAction.data as string;
			const card = data.cards.find((c) => c.ticker === ticker);
			const cost = card ? Math.ceil(card.health / 2) : 0;
			addLog(`Bot deployed ${getCreatureName(ticker)}! (-${cost} HP)`, 'deploy');
		} else if (botAction.actionType === 'attack') {
			const atk = botAction.data as Attack;
			const attacker = data.cards.find((c) => c.ticker === atk.attacker);
			const defender = data.cards.find((c) => c.ticker === atk.opponent);
			if (attacker && defender) {
				const superEff = isSuperEffective(attacker.sector, defender.sector);
				const baseDmg = Math.max(attacker.attack - defender.defense, 1);
				const dmg = superEff ? Math.floor(baseDmg * 2) : baseDmg;
				const counter = Math.max(defender.attack - attacker.defense, 1);
				addLog(`Bot's ${getCreatureName(atk.attacker)} attacked ${getCreatureName(atk.opponent)} for ${dmg} damage!`, 'damage');
				addLog(`${getCreatureName(atk.opponent)} countered for ${counter} damage!`, 'damage');
				if (superEff) addLog('Super effective!', 'super');
			}
		} else if (botAction.actionType === 'attack-face') {
			const ticker = botAction.data as string;
			const attacker = data.cards.find((c) => c.ticker === ticker);
			const dmg = attacker?.attack || 0;
			addLog(`Bot's ${getCreatureName(ticker)} attacked you directly for ${dmg} damage!`, 'damage');
		} else if (botAction.actionType === 'grow') {
			addLog(`Bot grew ${getCreatureName(botAction.data as string)}.`, 'system');
		}
	}

	function playCard(cardTicker: string) {
		if (gameState.whosTurn !== 'you') return;
		const cardDef = data.cards.find(({ ticker }) => ticker === cardTicker);
		const hp = cardDef?.health || 0;
		const cost = Math.ceil(hp / 2);
		if (cost >= gameState.you.health) {
			showNotification('Not enough HP to deploy this creature.');
			return;
		}
		if (gameState.you.inPlay.length >= FIELD_SLOTS) {
			showNotification('Field is full!');
			return;
		}
		addLog(`You deployed ${getCreatureName(cardTicker)}! (-${cost} HP)`, 'deploy');

		const action: Action = { actionType: 'play', data: cardTicker };
		const result = updateGameState(gameState, action, data.cards);
		gameState = result.state;
		selectedCard = null;
		actionMode = 'idle';

		if (!gameState.winner) logBotAction(result.botAction);
	}

	function growCard(cardTicker: string) {
		addLog(`${getCreatureName(cardTicker)} used Grow!`, 'system');

		const action: Action = { actionType: 'grow', data: cardTicker };
		const result = updateGameState(gameState, action, data.cards);
		gameState = result.state;
		selectedCard = null;
		actionMode = 'idle';

		if (!gameState.winner) logBotAction(result.botAction);
	}

	function attackCard(attackerTicker: string, opponentTicker: string) {
		const attacker = data.cards.find((c) => c.ticker === attackerTicker);
		const defender = data.cards.find((c) => c.ticker === opponentTicker);
		const superEff = attacker && defender && isSuperEffective(attacker.sector, defender.sector);

		const baseDmg = attacker && defender ? Math.max(attacker.attack - defender.defense, 1) : 1;
		const dmg = superEff ? Math.floor(baseDmg * 2) : baseDmg;
		const counter = attacker && defender ? Math.max(defender.attack - attacker.defense, 1) : 1;

		addLog(
			`${getCreatureName(attackerTicker)} attacked ${getCreatureName(opponentTicker)} for ${dmg} damage!`,
			'damage'
		);
		addLog(
			`${getCreatureName(opponentTicker)} countered for ${counter} damage!`,
			'damage'
		);
		if (superEff) {
			addLog('Super effective!', 'super');
			showNotification(
				`Super effective! ${attacker?.sector} \u2192 ${defender?.sector} (2\u00D7 damage)`,
				'success'
			);
		}

		const action: Action = {
			actionType: 'attack',
			data: { attacker: attackerTicker, opponent: opponentTicker }
		};
		const result = updateGameState(gameState, action, data.cards);
		gameState = result.state;
		selectedCard = null;
		actionMode = 'idle';

		if (!gameState.winner) logBotAction(result.botAction);
	}

	function attackFace(attackerTicker: string) {
		const attacker = data.cards.find((c) => c.ticker === attackerTicker);
		const dmg = attacker?.attack || 0;
		addLog(`${getCreatureName(attackerTicker)} attacked opponent directly for ${dmg} damage!`, 'damage');

		const action: Action = { actionType: 'attack-face', data: attackerTicker };
		const result = updateGameState(gameState, action, data.cards);
		gameState = result.state;
		selectedCard = null;
		actionMode = 'idle';

		if (!gameState.winner) logBotAction(result.botAction);
	}

	function handleFaceClick() {
		if (actionMode === 'select-target' && selectedCard && gameState.opponent.inPlay.length === 0) {
			attackFace(selectedCard);
		}
	}

	function handleFieldClick(ticker: string | null, side: 'player' | 'opponent') {
		if (gameState.whosTurn !== 'you' || !ticker) return;

		if (side === 'player') {
			if (actionMode === 'select-target') {
				// Clicking own card while selecting target cancels
				selectedCard = null;
				actionMode = 'idle';
				return;
			}
			if (selectedCard === ticker) {
				selectedCard = null;
				actionMode = 'idle';
			} else {
				selectedCard = ticker;
				actionMode = 'select-action';
			}
		} else if (side === 'opponent') {
			if (actionMode === 'select-target' && selectedCard) {
				attackCard(selectedCard, ticker);
			}
		}
	}

	function startAttackMode() {
		actionMode = 'select-target';
	}

	function cancelAction() {
		selectedCard = null;
		actionMode = 'idle';
	}

	// Build padded slot arrays
	$: playerSlots = Array.from({ length: Math.max(FIELD_SLOTS, gameState.you.inPlay.length) }, (_, i) =>
		gameState.you.inPlay[i] || null
	);
	$: opponentSlots = Array.from(
		{ length: Math.max(FIELD_SLOTS, gameState.opponent.inPlay.length) },
		(_, i) => gameState.opponent.inPlay[i] || null
	);

	// Fan effect angles for hand cards
	function fanAngle(index: number, total: number): number {
		if (total <= 1) return 0;
		const spread = Math.min(total * 3, 15);
		return -spread / 2 + (spread / (total - 1)) * index;
	}

	function fanY(index: number, total: number): number {
		if (total <= 1) return 0;
		const mid = (total - 1) / 2;
		const dist = Math.abs(index - mid) / mid;
		return dist * dist * 12;
	}
</script>

<svelte:window bind:innerWidth />

<div class="arena-page">
	<!-- Header -->
	<div class="arena-header">
		<a href="/" class="exit-link font-mono">&larr; Exit</a>
		<span class="arena-title font-display text-gold">ARENA</span>
		{#if !gameState.winner}
			<span class="turn-tag font-mono" class:your-turn={gameState.whosTurn === 'you'} transition:fade|local={{ duration: 200 }}>
				{gameState.whosTurn === 'you' ? 'YOUR TURN' : 'BOT TURN'}
			</span>
		{:else}
			<div style="width: 72px"></div>
		{/if}
	</div>

	<!-- Game Mat -->
	<div class="game-mat">
		<!-- Opponent HUD -->
		<div class="mat-row hud-row">
			<PlayerHud
				label="BOT"
				health={gameState.opponent.health}
				maxHealth={MAX_HEALTH}
				isActive={gameState.whosTurn === 'opponent'}
				side="opponent"
				isAttackTarget={actionMode === 'select-target' && gameState.opponent.inPlay.length === 0}
				on:click={handleFaceClick}
			/>
		</div>

		<!-- Opponent Field -->
		<div class="mat-row field-row">
			{#each opponentSlots as card, i (card ? card.ticker : `op-empty-${i}`)}
				{@const cardData = card ? data.cards.find((c) => c.ticker === card.ticker) : undefined}
				<CardSlot
					{card}
					{cardData}
					isSelected={false}
					isAttackTarget={actionMode === 'select-target' && card !== null}
					isPlayerSide={false}
					slotIndex={i}
					sizeMultiplier={fieldCardSize}
					on:click={() => handleFieldClick(card?.ticker || null, 'opponent')}
				/>
			{/each}
		</div>

		<!-- Divider -->
		<div class="mat-row divider-row">
			<div class="div-line"></div>
			<span class="div-vs font-display">VS</span>
			<div class="div-line"></div>
		</div>

		<!-- Player Field -->
		<div class="mat-row field-row">
			{#each playerSlots as card, i (card ? card.ticker : `pl-empty-${i}`)}
				{@const cardData = card ? data.cards.find((c) => c.ticker === card.ticker) : undefined}
				<CardSlot
					{card}
					{cardData}
					isSelected={selectedCard === card?.ticker}
					isAttackTarget={false}
					isPlayerSide={true}
					slotIndex={i}
					sizeMultiplier={fieldCardSize}
					on:click={() => handleFieldClick(card?.ticker || null, 'player')}
				/>
			{/each}
		</div>

		<!-- Player HUD -->
		<div class="mat-row hud-row">
			<PlayerHud
				label="YOU"
				health={gameState.you.health}
				maxHealth={MAX_HEALTH}
				isActive={gameState.whosTurn === 'you'}
				side="player"
			/>
		</div>
	</div>

	<!-- Action Panel -->
	{#if actionMode === 'select-action' && selectedCard}
		{@const sel = data.cards.find((c) => c.ticker === selectedCard)}
		<div class="action-panel" transition:slide|local={{ duration: 200, easing: quintOut }}>
			<span class="act-label font-mono">{sel?.creatureName || selectedCard}</span>
			<div class="act-btns">
				<button class="act grow" on:click={() => growCard(selectedCard || '')}>
					Grow
				</button>
				<button class="act attack" on:click={startAttackMode}>
					{gameState.opponent.inPlay.length === 0 ? 'Attack Face' : 'Attack'}
				</button>
				<button class="act cancel" on:click={cancelAction}>Cancel</button>
			</div>
		</div>
	{/if}

	{#if actionMode === 'select-target'}
		<div class="action-panel target-mode" transition:slide|local={{ duration: 200, easing: quintOut }}>
			<span class="act-label font-mono" style="color: var(--red)">
				{gameState.opponent.inPlay.length === 0 ? 'CLICK OPPONENT TO ATTACK' : 'SELECT TARGET'}
			</span>
			<button class="act cancel" on:click={cancelAction}>Cancel</button>
		</div>
	{/if}

	<!-- Hand (always visible) -->
	<div class="hand-area">
		<div class="hand-label font-mono">HAND [{gameState.you.hand.length}]</div>
		{#if gameState.you.hand.length === 0}
			<div class="hand-empty font-mono">HAND EMPTY</div>
		{:else}
			<div class="hand-scroll" class:fan={innerWidth >= 768}>
				{#each gameState.you.hand as cardTicker, i (cardTicker)}
					{@const cardData = data.cards.find((card) => card.ticker === cardTicker)}
					{@const total = gameState.you.hand.length}
					{@const cost = cardData ? Math.ceil(cardData.health / 2) : 0}
					{@const canAfford = cost < gameState.you.health}
					<div
						class="hand-card"
						class:disabled={gameState.whosTurn !== 'you'}
						class:unaffordable={!canAfford}
						style={innerWidth >= 768
							? `--fan-angle: ${fanAngle(i, total)}deg; --fan-y: ${fanY(i, total)}px;`
							: ''}
						transition:scale|local={{ duration: 300, easing: quintOut, start: 0.8 }}
					>
						<Card
							name={cardData?.creatureName || ''}
							health={cardData?.health || 0}
							defense={cardData?.defense || 0}
							attack={cardData?.attack || 0}
							growth={cardData?.growth || 0}
							on:click={() => playCard(cardTicker)}
							company={cardData?.name || ''}
							ticker={cardTicker}
							sector={cardData?.sector || ''}
							sizeMultiplier={handCardSize}
						/>
						<span class="deploy-cost font-mono">-{cost} HP</span>
					</div>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Mobile ticker (shows inside flow) -->
	<BattleLog messages={battleLog} />

	<!-- Toast -->
	{#if notification}
		<div
			class="toast font-mono"
			class:toast-success={notificationType === 'success'}
			transition:fade|local={{ duration: 200 }}
		>
			{notification}
		</div>
	{/if}

	<!-- Game Over -->
	{#if gameState.winner}
		<div class="game-over" transition:fade|local={{ duration: 400 }}>
			<div
				class="go-card"
				class:win={gameState.winner === 'you'}
				class:lose={gameState.winner === 'opponent'}
			>
				{#if gameState.winner === 'you'}
					<p class="go-tag font-mono green">VICTORY</p>
					<h2 class="go-title font-display">You Win</h2>
					<p class="go-sub">Your portfolio dominated the arena.</p>
				{:else}
					<p class="go-tag font-mono red">DEFEAT</p>
					<h2 class="go-title font-display">You Lose</h2>
					<p class="go-sub">The market had other plans.</p>
				{/if}
				<div class="go-btns">
					<a href="/play" class="go-btn go-primary font-display">Play Again</a>
					<a href="/" class="go-btn go-secondary">Home</a>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	/* ---- Full viewport layout ---- */
	.arena-page {
		position: relative;
		z-index: 1;
		height: 100vh;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	/* ---- Header ---- */
	.arena-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.5rem 1.25rem;
		background: rgba(6, 6, 10, 0.85);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-bottom: 1px solid var(--border);
		z-index: 10;
		flex-shrink: 0;
	}

	.exit-link {
		color: var(--text-muted);
		text-decoration: none;
		font-size: 0.75rem;
		font-weight: 600;
		transition: color 0.2s;
	}

	.exit-link:hover {
		color: var(--text-primary);
	}

	.arena-title {
		font-size: 0.9rem;
		font-weight: 700;
		letter-spacing: 0.15em;
	}

	.turn-tag {
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		padding: 0.25rem 0.6rem;
		border-radius: 0.3rem;
		background: rgba(255, 255, 255, 0.04);
		border: 1px solid var(--border);
		color: var(--text-muted);
	}

	.turn-tag.your-turn {
		background: rgba(201, 168, 76, 0.1);
		border-color: rgba(201, 168, 76, 0.3);
		color: var(--gold);
		animation: turnGlow 2s ease-in-out infinite;
	}

	@keyframes turnGlow {
		0%, 100% { box-shadow: 0 0 4px rgba(201, 168, 76, 0.1); }
		50% { box-shadow: 0 0 12px rgba(201, 168, 76, 0.2); }
	}

	/* ---- Game Mat ---- */
	.game-mat {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0.5rem 1rem;
		gap: 0.35rem;
		overflow-y: auto;
		max-width: 1000px;
		width: 100%;
		margin: 0 auto;
		min-height: 0;
	}

	.mat-row {
		width: 100%;
		flex-shrink: 0;
	}

	.hud-row {
		max-width: 600px;
		margin: 0 auto;
		width: 100%;
	}

	/* ---- Field Rows ---- */
	.field-row {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 0.5rem;
		flex-wrap: wrap;
		padding: 0.25rem 0;
		flex: 1;
		min-height: 0;
	}

	/* ---- Divider ---- */
	.divider-row {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.1rem 0;
		flex-shrink: 0;
		flex: 0;
	}

	.div-line {
		flex: 1;
		height: 1px;
		background: linear-gradient(to right, transparent, var(--border), transparent);
	}

	.div-vs {
		font-size: 0.65rem;
		font-weight: 700;
		letter-spacing: 0.2em;
		color: var(--gold-dim);
	}

	/* ---- Action Panel ---- */
	.action-panel {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		padding: 0.45rem 1rem;
		background: rgba(6, 6, 10, 0.92);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-top: 1px solid var(--border);
		flex-shrink: 0;
		flex-wrap: wrap;
	}

	.action-panel.target-mode {
		border-top-color: rgba(255, 71, 87, 0.3);
		background: rgba(255, 71, 87, 0.04);
	}

	.act-label {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		color: var(--purple-glow);
		white-space: nowrap;
	}

	.act-btns {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.act {
		padding: 0.4rem 0.9rem;
		border-radius: 0.375rem;
		border: 1px solid transparent;
		font-family: 'DM Sans', sans-serif;
		font-size: 0.75rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.2s ease;
		white-space: nowrap;
	}

	.act.grow {
		background: rgba(0, 212, 123, 0.12);
		color: var(--green);
		border-color: rgba(0, 212, 123, 0.25);
	}

	.act.grow:hover {
		background: rgba(0, 212, 123, 0.2);
		transform: translateY(-1px);
	}

	.act.attack {
		background: rgba(255, 71, 87, 0.1);
		color: var(--red);
		border-color: rgba(255, 71, 87, 0.2);
	}

	.act.attack:hover {
		background: rgba(255, 71, 87, 0.18);
		transform: translateY(-1px);
	}

	.act.cancel {
		background: transparent;
		color: var(--text-muted);
		border-color: var(--border);
	}

	.act.cancel:hover {
		color: var(--text-secondary);
		background: rgba(255, 255, 255, 0.03);
	}

	/* ---- Hand Area (always visible) ---- */
	.hand-area {
		flex-shrink: 0;
		background: rgba(6, 6, 10, 0.92);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-top: 1px solid rgba(201, 168, 76, 0.15);
		padding: 0.4rem 0;
	}

	.hand-label {
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		color: var(--gold-dim);
		padding: 0 1rem 0.25rem;
	}

	.hand-scroll {
		display: flex;
		gap: 0.6rem;
		overflow-x: auto;
		padding: 0.25rem 1.25rem 0.5rem;
		justify-content: flex-start;
	}

	.hand-scroll::-webkit-scrollbar { height: 3px; }
	.hand-scroll::-webkit-scrollbar-track { background: transparent; }
	.hand-scroll::-webkit-scrollbar-thumb { background: rgba(201, 168, 76, 0.15); border-radius: 3px; }

	/* Fan effect on desktop */
	.hand-scroll.fan {
		justify-content: center;
		overflow-x: visible;
		gap: 0.35rem;
	}

	.hand-scroll.fan .hand-card {
		transform: rotate(var(--fan-angle, 0deg)) translateY(var(--fan-y, 0px));
		transition: transform 0.3s ease;
	}

	.hand-scroll.fan .hand-card:hover {
		transform: rotate(0deg) translateY(-14px) !important;
		z-index: 5;
	}

	.hand-card {
		flex-shrink: 0;
		cursor: pointer;
		border-radius: 1.25rem;
		padding: 2px;
		border: 2px solid transparent;
		transition: transform 0.2s ease, border-color 0.2s ease;
		position: relative;
	}

	.hand-card:hover {
		border-color: rgba(201, 168, 76, 0.3);
	}

	.hand-card.disabled {
		opacity: 0.5;
		pointer-events: none;
	}

	.hand-card.unaffordable {
		opacity: 0.4;
		filter: grayscale(0.5);
	}

	.deploy-cost {
		position: absolute;
		top: 6px;
		right: 8px;
		background: rgba(255, 71, 87, 0.85);
		color: #fff;
		font-size: 0.55rem;
		font-weight: 700;
		padding: 1px 5px;
		border-radius: 4px;
		letter-spacing: 0.02em;
		z-index: 4;
		pointer-events: none;
	}

	.hand-empty {
		text-align: center;
		padding: 0.75rem;
		color: var(--text-muted);
		font-size: 0.65rem;
		letter-spacing: 0.15em;
	}

	/* ---- Toast ---- */
	.toast {
		position: fixed;
		top: 1rem;
		left: 50%;
		transform: translateX(-50%);
		padding: 0.6rem 1.25rem;
		border-radius: 0.375rem;
		background: rgba(255, 71, 87, 0.12);
		border: 1px solid rgba(255, 71, 87, 0.3);
		color: var(--red);
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.05em;
		z-index: 40;
		pointer-events: none;
	}

	.toast.toast-success {
		background: rgba(0, 212, 123, 0.12);
		border-color: rgba(0, 212, 123, 0.3);
		color: var(--green);
	}

	/* ---- Game Over ---- */
	.game-over {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.75);
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 50;
	}

	.go-card {
		text-align: center;
		padding: 3rem 3.5rem;
		border-radius: 1rem;
		border: 1px solid;
		animation: scaleIn 0.45s ease-out both;
	}

	@keyframes scaleIn {
		from { transform: scale(0.85); opacity: 0; }
		to { transform: scale(1); opacity: 1; }
	}

	.go-card.win {
		background: var(--bg-surface);
		border-color: rgba(0, 212, 123, 0.3);
		box-shadow: 0 0 40px rgba(0, 212, 123, 0.1);
	}

	.go-card.lose {
		background: var(--bg-surface);
		border-color: rgba(255, 71, 87, 0.3);
		box-shadow: 0 0 40px rgba(255, 71, 87, 0.1);
	}

	.go-tag {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.2em;
		margin-bottom: 0.5rem;
	}

	.go-tag.green { color: var(--green); }
	.go-tag.red { color: var(--red); }

	.go-title {
		font-size: 2.5rem;
		font-weight: 900;
		letter-spacing: 0.04em;
		margin-bottom: 0.4rem;
	}

	.go-card.win .go-title { color: var(--green); }
	.go-card.lose .go-title { color: var(--red); }

	.go-sub {
		color: var(--text-secondary);
		font-size: 0.95rem;
		margin-bottom: 2rem;
	}

	.go-btns {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
	}

	.go-btn {
		padding: 0.75rem 1.75rem;
		border-radius: 0.5rem;
		text-decoration: none;
		font-weight: 700;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.go-primary {
		background: linear-gradient(135deg, #c9a84c, #a8873a);
		color: #0a0a12;
		box-shadow: 0 0 16px rgba(201, 168, 76, 0.2);
		letter-spacing: 0.04em;
	}

	.go-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 0 24px rgba(201, 168, 76, 0.3);
	}

	.go-secondary {
		background: transparent;
		border: 1px solid var(--border);
		color: var(--text-secondary);
	}

	.go-secondary:hover {
		border-color: var(--border-hover);
		color: var(--text-primary);
	}

	/* ---- Responsive ---- */
	@media (max-width: 768px) {
		.game-mat { padding: 0.35rem 0.5rem; gap: 0.25rem; }
		.field-row { gap: 0.35rem; }
		.hand-scroll { padding: 0.25rem 0.75rem 0.5rem; gap: 0.5rem; }
		.go-card { padding: 2rem 1.5rem; }
		.go-title { font-size: 2rem; }
		.go-btns { flex-direction: column; align-items: center; }
		.go-btn { width: 100%; max-width: 220px; text-align: center; }
		.toast { max-width: 90vw; text-align: center; font-size: 0.7rem; }
	}

	@media (max-width: 480px) {
		.arena-header { padding: 0.4rem 0.75rem; }
		.arena-title { font-size: 0.8rem; }
		.turn-tag { font-size: 0.55rem; padding: 0.2rem 0.4rem; }
		.game-mat { padding: 0.25rem 0.35rem; gap: 0.2rem; }
		.field-row { gap: 0.25rem; padding: 0.15rem 0; }
		.action-panel { padding: 0.35rem 0.75rem; gap: 0.5rem; }
		.act { padding: 0.35rem 0.7rem; font-size: 0.7rem; }
		.hand-label { font-size: 0.55rem; padding: 0 0.75rem 0.2rem; }
		.hand-scroll { padding: 0.2rem 0.5rem 0.4rem; gap: 0.35rem; }
		.go-card { padding: 1.75rem 1.25rem; margin: 0 1rem; }
		.go-title { font-size: 1.75rem; }
		.go-sub { font-size: 0.85rem; margin-bottom: 1.5rem; }
	}
</style>
