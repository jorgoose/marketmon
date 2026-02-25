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

		<!-- Weakness Chart -->
		<div class="weakness-section">
			<h2 class="section-title font-display text-gold">Sector Weaknesses</h2>
			<p class="about-body">
				Each sector type is strong against one other and weak to one other.
				Attacks against a weak type deal <span class="font-mono hl-green">1.5x</span> damage.
			</p>

			<div class="weakness-cycle">
				<div class="wk-row">
					<span class="wk-type font-mono" style="color: #00c2ff">Technology</span>
					<span class="wk-arrow">&rarr;</span>
					<span class="wk-type font-mono" style="color: #f97316">Comm. Services</span>
					<span class="wk-arrow">&rarr;</span>
					<span class="wk-type font-mono" style="color: #68b77b">Consumer Def.</span>
				</div>
				<div class="wk-connector">&darr;</div>
				<div class="wk-row">
					<span class="wk-type font-mono" style="color: #a8876a">Materials</span>
					<span class="wk-arrow">&larr;</span>
					<span class="wk-type font-mono" style="color: #a855f7">Consumer Cyc.</span>
					<span class="wk-arrow">&larr;</span>
					<span class="wk-type font-mono" style="color: #2a6dd4">Financial Svcs.</span>
				</div>
				<div class="wk-connector">&uarr;</div>
				<div class="wk-row">
					<span class="wk-type font-mono" style="color: #c2873a">Real Estate</span>
					<span class="wk-arrow">&larr;</span>
					<span class="wk-type font-mono" style="color: #64748b">Utilities</span>
					<span class="wk-arrow">&larr;</span>
					<span class="wk-type font-mono" style="color: #ff6b1a">Energy</span>
				</div>
				<div class="wk-connector">&uarr;</div>
				<div class="wk-row wk-row-center">
					<span class="wk-type font-mono" style="color: #e5457b">Healthcare</span>
					<span class="wk-arrow">&rarr;</span>
					<span class="wk-type font-mono" style="color: #d4a017">Industrials</span>
					<span class="wk-arrow wk-arrow-up">&uarr;</span>
				</div>
			</div>

			<div class="weakness-list">
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #00c2ff">TECH</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #f97316">COMM</span>
					<span class="wk-reason">Tech platforms disrupt telecom &amp; media</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #f97316">COMM</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #68b77b">C.DEF</span>
					<span class="wk-reason">Advertising undermines generic staple brands</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #68b77b">C.DEF</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #e5457b">HLTH</span>
					<span class="wk-reason">Preventive wellness reduces healthcare need</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #e5457b">HLTH</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #d4a017">IND</span>
					<span class="wk-reason">Health regulations constrain industry</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #d4a017">IND</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #ff6b1a">NRG</span>
					<span class="wk-reason">Renewables manufacturing displaces fossil fuels</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #ff6b1a">NRG</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #64748b">UTIL</span>
					<span class="wk-reason">Energy price spikes crush utility margins</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #64748b">UTIL</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #c2873a">RE</span>
					<span class="wk-reason">Rising utility costs burden property operations</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #c2873a">RE</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #2a6dd4">FIN</span>
					<span class="wk-reason">Real estate crashes devastate banks</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #2a6dd4">FIN</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #a855f7">C.CYC</span>
					<span class="wk-reason">Credit tightening chokes discretionary spending</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #a855f7">C.CYC</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #a8876a">MAT</span>
					<span class="wk-reason">Demand volatility destabilizes material suppliers</span>
				</div>
				<div class="wk-item">
					<span class="wk-from font-mono" style="color: #a8876a">MAT</span>
					<span class="wk-beats">&rarr;</span>
					<span class="wk-to font-mono" style="color: #00c2ff">TECH</span>
					<span class="wk-reason">Rare earth scarcity constrains tech production</span>
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

	/* ---- Weakness Section ---- */
	.weakness-section {
		animation: fadeUp 0.5s ease-out 0.45s both;
		margin-bottom: 3rem;
	}

	.weakness-cycle {
		padding: 1.5rem;
		border-radius: 0.75rem;
		background: rgba(10, 10, 18, 0.5);
		border: 1px solid var(--border);
		margin-bottom: 1.5rem;
	}

	.wk-row {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
	}

	.wk-row-center {
		justify-content: center;
	}

	.wk-type {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		padding: 0.3rem 0.6rem;
		border-radius: 0.25rem;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.08);
		white-space: nowrap;
	}

	.wk-arrow {
		color: var(--gold-dim);
		font-size: 0.8rem;
		flex-shrink: 0;
	}

	.wk-arrow-up {
		color: var(--gold-dim);
	}

	.wk-connector {
		text-align: center;
		color: var(--gold-dim);
		font-size: 0.8rem;
		padding: 0.15rem 0;
		line-height: 1;
	}

	.weakness-list {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.wk-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.75rem;
		border-radius: 0.375rem;
		background: rgba(10, 10, 18, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.04);
		font-size: 0.72rem;
	}

	.wk-from, .wk-to {
		font-weight: 700;
		letter-spacing: 0.06em;
		min-width: 3rem;
	}

	.wk-beats {
		color: var(--gold-dim);
		flex-shrink: 0;
	}

	.wk-reason {
		color: var(--text-muted);
		font-size: 0.7rem;
		margin-left: auto;
		text-align: right;
	}

	@media (max-width: 768px) {
		.guide-page { padding: 2rem 1.25rem 4rem; }
		.guide-hero { margin-bottom: 2rem; }
		.weakness-cycle { padding: 1rem; }
	}

	@media (max-width: 500px) {
		.data-grid { grid-template-columns: 1fr; }
		.step { flex-direction: column; gap: 0.75rem; }
		.step { padding: 1.25rem; }
		.wk-reason { display: none; }
		.wk-row { gap: 0.3rem; }
		.wk-type { font-size: 0.6rem; padding: 0.25rem 0.4rem; }
		.guide-title { font-size: 1.75rem; }
		.section-title { font-size: 1.25rem; }
		.guide-page { padding: 1.5rem 1rem 3rem; }
		.weakness-cycle { padding: 0.75rem; overflow-x: auto; -webkit-overflow-scrolling: touch; }
		.wk-item { font-size: 0.65rem; padding: 0.4rem 0.5rem; gap: 0.35rem; }
	}
</style>
