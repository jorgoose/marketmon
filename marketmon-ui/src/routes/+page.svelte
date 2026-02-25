<script lang="ts">
	import Card from './Card.svelte';
	import Navbar from './Navbar.svelte';
	import type { PageServerData } from './$types';

	export let data: PageServerData;

	const cards = data.cards;
</script>

<div class="page">
	<Navbar />

	<!-- Hero -->
	<section class="hero">
		<div class="hero-content">
			<p class="hero-tag font-mono">S&P 500 &times; TRADING CARD GAME</p>
			<h1 class="hero-title font-display">
				Deploy. Duel.<br />
				<span class="text-gold">Dominate.</span>
			</h1>
			<p class="hero-sub">
				500+ creatures forged from real market data.
				Every stat backed by fundamentals. Every battle shaped by the index.
			</p>
			<div class="hero-actions">
				<a href="/play" class="btn-gold font-display">Enter the Arena</a>
				<a href="/cards" class="btn-ghost">Browse the Index</a>
			</div>
		</div>

		<!-- Terminal-style stat strip -->
		<div class="stat-strip font-mono">
			<div class="stat-cell">
				<span class="stat-val">503</span>
				<span class="stat-key">CREATURES</span>
			</div>
			<span class="stat-sep">|</span>
			<div class="stat-cell">
				<span class="stat-val">11</span>
				<span class="stat-key">SECTORS</span>
			</div>
			<span class="stat-sep">|</span>
			<div class="stat-cell">
				<span class="stat-val green">&bull; LIVE</span>
				<span class="stat-key">MARKET DATA</span>
			</div>
		</div>
	</section>

	<!-- Features -->
	<section class="features">
		<div class="feat">
			<h3 class="feat-title font-display">Market-Driven Stats</h3>
			<p class="feat-body">
				Market cap, free cash flow, shareholder equity, and earnings growth
				are translated directly into card stats. The market moves &mdash; your deck evolves.
			</p>
		</div>
		<div class="feat">
			<h3 class="feat-title font-display">Strategic Combat</h3>
			<p class="feat-body">
				Deploy creatures, grow their power, and attack your opponent's field.
				Every move costs something. Resource management wins games.
			</p>
		</div>
		<div class="feat">
			<h3 class="feat-title font-display">Full Index Coverage</h3>
			<p class="feat-body">
				Every company in the S&P 500 has a unique AI-generated creature.
				From <span class="font-mono">AAPL</span> to <span class="font-mono">ZTS</span> &mdash; collect them all.
			</p>
		</div>
	</section>

	<!-- Carousel -->
	<section class="carousel-section">
		<h2 class="carousel-title font-display">The Index</h2>
		<div class="carousel-wrapper">
			<div class="carousel-fade carousel-fade-left"></div>
			<div class="carousel-track">
				{#each cards as card}
					<Card
						sizeMultiplier={0.9}
						name={card.creatureName}
						health={card.health || 0}
						defense={card.defense || 0}
						attack={card.attack || 0}
						growth={card.growth || 0}
						company={card.name}
						ticker={card.ticker}
						sector={card.sector}
					/>
				{/each}
			</div>
			<div class="carousel-fade carousel-fade-right"></div>
		</div>
	</section>

	<!-- Footer -->
	<footer class="site-footer">
		<span class="footer-brand font-display text-gold">Marketmon</span>
		<span class="footer-copy">&copy; 2024 &middot; Where the index meets the arena.</span>
	</footer>
</div>

<style>
	.page {
		position: relative;
		z-index: 1;
		overflow: hidden;
	}

	/* ---- Hero ---- */
	.hero {
		max-width: 820px;
		margin: 0 auto;
		padding: 6rem 1.5rem 3.5rem;
		text-align: center;
	}

	.hero-tag {
		font-size: 0.7rem;
		letter-spacing: 0.2em;
		color: var(--gold);
		margin-bottom: 1.25rem;
		animation: fadeUp 0.5s ease-out 0.05s both;
	}

	.hero-title {
		font-size: clamp(2.5rem, 6vw, 4.25rem);
		font-weight: 900;
		line-height: 1.1;
		letter-spacing: 0.03em;
		margin-bottom: 1.25rem;
		animation: fadeUp 0.5s ease-out 0.15s both;
	}

	.hero-sub {
		font-size: 1.05rem;
		color: var(--text-secondary);
		line-height: 1.7;
		max-width: 500px;
		margin: 0 auto 2.5rem;
		animation: fadeUp 0.5s ease-out 0.25s both;
	}

	.hero-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		animation: fadeUp 0.5s ease-out 0.35s both;
	}

	.btn-gold {
		display: inline-block;
		padding: 0.85rem 2.25rem;
		background: linear-gradient(135deg, #c9a84c, #a8873a);
		color: #0a0a12;
		font-weight: 700;
		font-size: 0.9rem;
		letter-spacing: 0.06em;
		border-radius: 0.5rem;
		text-decoration: none;
		transition: all 0.25s ease;
		box-shadow: 0 0 20px rgba(201, 168, 76, 0.2), 0 4px 12px rgba(0, 0, 0, 0.4);
	}

	.btn-gold:hover {
		transform: translateY(-2px);
		box-shadow: 0 0 32px rgba(201, 168, 76, 0.3), 0 8px 20px rgba(0, 0, 0, 0.5);
		background: linear-gradient(135deg, #e2c56d, #c9a84c);
	}

	.btn-ghost {
		display: inline-block;
		padding: 0.85rem 2rem;
		border: 1px solid rgba(201, 168, 76, 0.25);
		color: var(--gold);
		font-weight: 600;
		font-size: 0.9rem;
		border-radius: 0.5rem;
		text-decoration: none;
		transition: all 0.25s ease;
	}

	.btn-ghost:hover {
		border-color: rgba(201, 168, 76, 0.5);
		background: rgba(201, 168, 76, 0.06);
		transform: translateY(-2px);
	}

	/* ---- Terminal stat strip ---- */
	.stat-strip {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 1.25rem;
		margin-top: 4rem;
		padding: 1rem 2rem;
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		background: rgba(10, 10, 18, 0.6);
		font-size: 0.75rem;
		animation: fadeUp 0.5s ease-out 0.5s both;
	}

	.stat-cell {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.2rem;
	}

	.stat-val {
		font-weight: 700;
		color: var(--text-primary);
		font-size: 0.9rem;
	}

	.stat-val.green {
		color: var(--green);
	}

	.stat-key {
		color: var(--text-muted);
		font-size: 0.65rem;
		letter-spacing: 0.12em;
	}

	.stat-sep {
		color: var(--text-muted);
		opacity: 0.4;
	}

	/* ---- Features ---- */
	.features {
		max-width: 1100px;
		margin: 0 auto;
		padding: 1rem 1.5rem 4rem;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.25rem;
	}

	.feat {
		padding: 1.75rem;
		border-radius: 0.75rem;
		background: rgba(18, 18, 30, 0.5);
		border: 1px solid var(--border);
		transition: all 0.3s ease;
	}

	.feat:hover {
		border-color: var(--border-hover);
		background: rgba(18, 18, 30, 0.8);
		box-shadow: 0 0 24px rgba(201, 168, 76, 0.06);
		transform: translateY(-4px);
	}

	.feat-title {
		font-size: 1rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		color: var(--gold-bright);
		margin-bottom: 0.6rem;
	}

	.feat-body {
		font-size: 0.88rem;
		color: var(--text-secondary);
		line-height: 1.65;
	}

	@media (max-width: 768px) {
		.features { grid-template-columns: 1fr; }
		.hero { padding: 3.5rem 1.5rem 2.5rem; }
		.stat-strip { flex-direction: column; gap: 0.75rem; }
		.stat-sep { display: none; }
	}

	/* ---- Carousel ---- */
	.carousel-section {
		padding: 1.5rem 0 5rem;
		overflow: hidden;
	}

	.carousel-title {
		text-align: center;
		font-size: 1.5rem;
		font-weight: 700;
		letter-spacing: 0.06em;
		margin-bottom: 1.5rem;
		color: var(--gold);
	}

	.carousel-wrapper {
		position: relative;
	}

	.carousel-fade {
		position: absolute;
		top: 0;
		bottom: 0;
		width: 140px;
		z-index: 2;
		pointer-events: none;
	}

	.carousel-fade-left {
		left: 0;
		background: linear-gradient(to right, var(--bg-void), transparent);
	}

	.carousel-fade-right {
		right: 0;
		background: linear-gradient(to left, var(--bg-void), transparent);
	}

	.carousel-track {
		white-space: nowrap;
		display: inline-flex;
		animation: slide 900s linear infinite;
		padding: 20px;
		gap: 8px;
	}

	@keyframes slide {
		0% { transform: translateX(0); }
		100% { transform: translateX(-50%); }
	}

	/* ---- Footer ---- */
	.site-footer {
		border-top: 1px solid var(--border);
		padding: 2rem 1.5rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.35rem;
	}

	.footer-brand {
		font-size: 1.1rem;
		font-weight: 700;
		letter-spacing: 0.06em;
	}

	.footer-copy {
		font-size: 0.75rem;
		color: var(--text-muted);
	}
</style>
