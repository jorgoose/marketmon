<script lang="ts">
	import Navbar from '../Navbar.svelte';
</script>

<div class="page">
	<Navbar />

	<div class="guide-page">
		<div class="guide-hero">
			<h1 class="guide-title font-display text-gold">Guide</h1>
			<p class="guide-sub font-mono">HOW TO PLAY MARKETMON</p>
		</div>

		<!-- Steps -->
		<div class="steps">
			<div class="step">
				<div class="step-num font-mono">01</div>
				<div class="step-body">
					<h3 class="step-title font-display">Draw Your Hand</h3>
					<p class="step-desc">
						Start with <span class="font-mono hl-green">50 HP</span> and 8 random creature cards
						drawn from the S&P 500. Each creature's stats reflect real financial data.
					</p>
				</div>
			</div>

			<div class="step">
				<div class="step-num font-mono">02</div>
				<div class="step-body">
					<h3 class="step-title font-display">Deploy Creatures</h3>
					<p class="step-desc">
						Play cards from your hand to the battlefield. Deploying costs HP equal to
						the creature's health stat. Overextend and you'll leave yourself vulnerable.
					</p>
				</div>
			</div>

			<div class="step">
				<div class="step-num font-mono">03</div>
				<div class="step-body">
					<h3 class="step-title font-display">Grow & Attack</h3>
					<p class="step-desc">
						<span class="hl-green">Grow</span> restores a creature's HP (overflow heals you).
						<span class="hl-red">Attack</span> deals your ATK minus their DEF as damage.
						Destroyed creatures leave the field.
					</p>
				</div>
			</div>

			<div class="step">
				<div class="step-num font-mono">04</div>
				<div class="step-body">
					<h3 class="step-title font-display">Win the Duel</h3>
					<p class="step-desc">
						Victory is achieved when your opponent has no valid moves remaining.
						Manage your health pool carefully &mdash; it fuels both deployment and survival.
					</p>
				</div>
			</div>
		</div>

		<div class="divider"></div>

		<!-- About -->
		<div class="about-section">
			<h2 class="section-title font-display text-gold">The Data</h2>
			<p class="about-body">
				Every Marketmon creature is derived from a real S&P 500 company.
				Card stats map directly to financial fundamentals:
			</p>

			<div class="data-grid">
				<div class="data-row">
					<span class="data-metric font-mono">MARKET_CAP</span>
					<span class="data-arrow">&rarr;</span>
					<span class="data-stat font-mono hl-red">HP</span>
				</div>
				<div class="data-row">
					<span class="data-metric font-mono">FREE_CASH_FLOW</span>
					<span class="data-arrow">&rarr;</span>
					<span class="data-stat font-mono hl-gold">ATK</span>
				</div>
				<div class="data-row">
					<span class="data-metric font-mono">SHAREHOLDER_EQ</span>
					<span class="data-arrow">&rarr;</span>
					<span class="data-stat font-mono hl-cyan">DEF</span>
				</div>
				<div class="data-row">
					<span class="data-metric font-mono">EARNINGS_GROWTH</span>
					<span class="data-arrow">&rarr;</span>
					<span class="data-stat font-mono hl-green">GRW</span>
				</div>
			</div>

			<p class="about-body">
				Creature names and images are AI-generated, giving each company a
				unique identity in the Marketmon universe. Real data, unreal battles.
			</p>
		</div>
	</div>
</div>

<style>
	.page {
		position: relative;
		z-index: 1;
		min-height: 100vh;
	}

	.guide-page {
		max-width: 660px;
		margin: 0 auto;
		padding: 3rem 1.5rem 5rem;
	}

	/* ---- Hero ---- */
	.guide-hero {
		text-align: center;
		margin-bottom: 3rem;
		animation: fadeUp 0.5s ease-out both;
	}

	.guide-title {
		font-size: 2.25rem;
		font-weight: 900;
		letter-spacing: 0.06em;
	}

	.guide-sub {
		font-size: 0.65rem;
		letter-spacing: 0.2em;
		color: var(--text-muted);
		margin-top: 0.4rem;
	}

	/* ---- Steps ---- */
	.steps {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-bottom: 3rem;
	}

	.step {
		display: flex;
		gap: 1.25rem;
		align-items: flex-start;
		padding: 1.5rem;
		border-radius: 0.75rem;
		background: rgba(18, 18, 30, 0.4);
		border: 1px solid var(--border);
		transition: all 0.25s ease;
		animation: fadeUp 0.5s ease-out both;
	}

	.step:nth-child(1) { animation-delay: 0.1s; }
	.step:nth-child(2) { animation-delay: 0.2s; }
	.step:nth-child(3) { animation-delay: 0.3s; }
	.step:nth-child(4) { animation-delay: 0.4s; }

	.step:hover {
		border-color: var(--border-hover);
		background: rgba(18, 18, 30, 0.6);
		box-shadow: 0 0 20px rgba(201, 168, 76, 0.04);
		transform: translateY(-3px);
	}

	.step-num {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		color: var(--gold-dim);
		min-width: 2rem;
		padding-top: 0.2rem;
	}

	.step-title {
		font-size: 1.05rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		color: var(--gold-bright);
		margin-bottom: 0.4rem;
	}

	.step-desc {
		color: var(--text-secondary);
		font-size: 0.9rem;
		line-height: 1.65;
	}

	.hl-green { color: var(--green); }
	.hl-red { color: var(--red); }
	.hl-gold { color: var(--gold); }
	.hl-cyan { color: var(--cyan); }

	/* ---- Divider ---- */
	.divider {
		height: 1px;
		background: linear-gradient(to right, transparent, var(--border), transparent);
		margin-bottom: 3rem;
	}

	/* ---- About ---- */
	.about-section {
		animation: fadeUp 0.5s ease-out 0.5s both;
	}

	.section-title {
		font-size: 1.5rem;
		font-weight: 900;
		letter-spacing: 0.06em;
		text-align: center;
		margin-bottom: 1rem;
	}

	.about-body {
		color: var(--text-secondary);
		font-size: 0.9rem;
		line-height: 1.7;
		margin-bottom: 1.25rem;
	}

	/* ---- Data Grid ---- */
	.data-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.6rem;
		margin: 1.5rem 0 1.75rem;
	}

	.data-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.6rem 0.9rem;
		border-radius: 0.375rem;
		background: rgba(10, 10, 18, 0.5);
		border: 1px solid var(--border);
		font-size: 0.72rem;
	}

	.data-metric {
		color: var(--text-muted);
		letter-spacing: 0.03em;
	}

	.data-arrow {
		color: var(--text-muted);
		opacity: 0.3;
	}

	.data-stat {
		font-weight: 700;
	}

	@media (max-width: 500px) {
		.data-grid { grid-template-columns: 1fr; }
		.step { flex-direction: column; gap: 0.75rem; }
	}
</style>
