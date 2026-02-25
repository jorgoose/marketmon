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
			<h1 class="hero-title font-display">
				<span class="title-yellow">Gotta Catch</span><br />
				<span class="title-white">Every Ticker!</span>
			</h1>
			<p class="hero-subtitle">
				500+ collectible creatures powered by the S&P 500.
				Real stocks. Real stats. Unreal battles.
			</p>
			<div class="hero-actions">
				<a href="/play" class="btn-play font-display">
					Start Battle!
				</a>
				<a href="/cards" class="btn-browse">
					Browse Cards
				</a>
			</div>
		</div>

		<div class="hero-stats">
			<div class="stat-bubble">
				<span class="stat-num font-display">500+</span>
				<span class="stat-label">Creatures</span>
			</div>
			<div class="stat-bubble">
				<span class="stat-num font-display">11</span>
				<span class="stat-label">Sectors</span>
			</div>
			<div class="stat-bubble">
				<span class="stat-num font-display">&infin;</span>
				<span class="stat-label">Battles</span>
			</div>
		</div>
	</section>

	<!-- Features -->
	<section class="features">
		<div class="feature-card fc-green">
			<div class="feature-badge font-display">Real Data</div>
			<p class="feature-text">
				Every card's stats come from real financial metrics &mdash; market cap, cash flow,
				equity, and growth.
			</p>
		</div>
		<div class="feature-card fc-red">
			<div class="feature-badge font-display">Battle!</div>
			<p class="feature-text">
				Deploy creatures, grow them, and attack your opponents in strategic turn-based combat.
			</p>
		</div>
		<div class="feature-card fc-yellow">
			<div class="feature-badge font-display">Collect</div>
			<p class="feature-text">
				From AAPL to ZTS &mdash; every S&P 500 company has a unique creature waiting
				to be discovered.
			</p>
		</div>
	</section>

	<!-- Carousel -->
	<section class="carousel-section">
		<h2 class="carousel-heading font-display">Meet the Creatures</h2>
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
		<p class="footer-text font-display">Marketmon</p>
		<p class="footer-copy">&copy; 2024 &middot; Where Wall Street meets the arena.</p>
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
		max-width: 800px;
		margin: 0 auto;
		padding: 5rem 1.5rem 3rem;
		text-align: center;
	}

	.hero-title {
		font-size: clamp(2.8rem, 7vw, 5rem);
		font-weight: 700;
		line-height: 1.1;
		margin-bottom: 1rem;
		animation: pop 0.6s ease-out both;
	}

	.title-yellow {
		color: var(--yellow);
		text-shadow: 0 3px 12px rgba(251, 191, 36, 0.35);
	}

	.title-white {
		color: #fff;
		text-shadow: 0 2px 16px rgba(0, 0, 0, 0.2);
	}

	.hero-subtitle {
		font-size: 1.15rem;
		color: rgba(255, 255, 255, 0.85);
		line-height: 1.6;
		max-width: 480px;
		margin: 0 auto 2rem;
		font-weight: 600;
		animation: fadeUp 0.5s ease-out 0.2s both;
	}

	.hero-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		animation: fadeUp 0.5s ease-out 0.35s both;
	}

	.btn-play {
		display: inline-block;
		padding: 1rem 2.5rem;
		background: var(--yellow);
		color: var(--blue-deep);
		font-weight: 700;
		font-size: 1.15rem;
		border-radius: 9999px;
		text-decoration: none;
		transition: all 0.2s ease;
		box-shadow: 0 4px 16px rgba(251, 191, 36, 0.35), 0 0 0 4px rgba(251, 191, 36, 0.15);
	}

	.btn-play:hover {
		transform: translateY(-3px) scale(1.03);
		box-shadow: 0 8px 24px rgba(251, 191, 36, 0.4), 0 0 0 6px rgba(251, 191, 36, 0.2);
	}

	.btn-browse {
		display: inline-flex;
		align-items: center;
		padding: 1rem 2rem;
		background: rgba(255, 255, 255, 0.12);
		border: 2px solid rgba(255, 255, 255, 0.25);
		color: #fff;
		font-weight: 700;
		font-size: 1rem;
		border-radius: 9999px;
		text-decoration: none;
		transition: all 0.2s ease;
	}

	.btn-browse:hover {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.4);
		transform: translateY(-2px);
	}

	/* ---- Stats ---- */
	.hero-stats {
		display: flex;
		justify-content: center;
		gap: 1.5rem;
		margin-top: 3.5rem;
		animation: bounceIn 0.5s ease-out 0.5s both;
	}

	.stat-bubble {
		background: rgba(255, 255, 255, 0.1);
		border: 2px solid rgba(255, 255, 255, 0.15);
		border-radius: 1rem;
		padding: 1rem 1.5rem;
		text-align: center;
		min-width: 100px;
		transition: transform 0.2s ease;
	}

	.stat-bubble:hover {
		transform: translateY(-4px);
		background: rgba(255, 255, 255, 0.15);
	}

	.stat-num {
		display: block;
		font-size: 1.75rem;
		font-weight: 700;
		color: var(--yellow);
	}

	.stat-label {
		font-size: 0.8rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: rgba(255, 255, 255, 0.7);
		margin-top: 0.15rem;
	}

	/* ---- Features ---- */
	.features {
		max-width: 1100px;
		margin: 0 auto;
		padding: 1rem 1.5rem 3rem;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.25rem;
	}

	.feature-card {
		padding: 1.75rem;
		border-radius: 1.25rem;
		background: rgba(255, 255, 255, 0.1);
		border: 2px solid rgba(255, 255, 255, 0.12);
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		transition: all 0.25s ease;
	}

	.feature-card:hover {
		transform: translateY(-6px);
		box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
	}

	.feature-badge {
		display: inline-block;
		padding: 0.3rem 0.9rem;
		border-radius: 9999px;
		font-size: 0.85rem;
		font-weight: 700;
		margin-bottom: 0.75rem;
	}

	.fc-green .feature-badge { background: var(--green); color: #052e16; }
	.fc-red .feature-badge { background: var(--red); color: #fff; }
	.fc-yellow .feature-badge { background: var(--yellow); color: #78350f; }

	.feature-text {
		font-size: 0.95rem;
		line-height: 1.6;
		color: rgba(255, 255, 255, 0.85);
		font-weight: 600;
	}

	@media (max-width: 768px) {
		.features { grid-template-columns: 1fr; }
		.hero { padding: 3rem 1.5rem 2rem; }
	}

	/* ---- Carousel ---- */
	.carousel-section {
		padding: 2rem 0 4rem;
		overflow: hidden;
	}

	.carousel-heading {
		text-align: center;
		font-size: 2rem;
		font-weight: 700;
		margin-bottom: 1.5rem;
		color: var(--yellow);
		text-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
	}

	.carousel-wrapper {
		position: relative;
	}

	.carousel-fade {
		position: absolute;
		top: 0;
		bottom: 0;
		width: 120px;
		z-index: 2;
		pointer-events: none;
	}

	.carousel-fade-left {
		left: 0;
		background: linear-gradient(to right, #2563eb, transparent);
	}

	.carousel-fade-right {
		right: 0;
		background: linear-gradient(to left, #2563eb, transparent);
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
		border-top: 2px solid rgba(255, 255, 255, 0.08);
		padding: 2rem 1.5rem;
		text-align: center;
	}

	.footer-text {
		font-size: 1.2rem;
		font-weight: 700;
		color: var(--yellow);
		margin-bottom: 0.25rem;
	}

	.footer-copy {
		font-size: 0.8rem;
		color: rgba(255, 255, 255, 0.45);
		font-weight: 600;
	}
</style>
