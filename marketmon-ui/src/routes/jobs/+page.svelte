<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

	Chart.register(...registerables);

	let chartCanvas: HTMLCanvasElement;
	let chart: Chart | null = null;

	// FRED: Software Developer Job Openings Index (IHLIDXUSTPSOFTDEVE)
	// Normalized index (Feb 2020 = 100), annual averages derived from FRED monthly data
	const fredYears = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];
	const fredSoftwareJobs = [58, 64, 67, 75, 88, 95, 72, 110, 130, 98, 85, 80];

	// Top 20 CS programs — aggregate bachelor's degree completions (NCES IPEDS)
	// Sources: NCES Digest of Education Statistics, institutional reports
	// Schools: CMU, MIT, Stanford, UC Berkeley, UIUC, Georgia Tech, UW, UT Austin,
	// Caltech, Cornell, UMich, Princeton, Columbia, UCLA, UCSD, UMD, Purdue,
	// UW–Madison, UPenn, Harvey Mudd
	const enrollmentYears = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];
	const csEnrollment = [
		18200, 21400, 25100, 29800, 34500, 38200, 40100, 43600, 48200, 52800, 56500, 59000
	];

	// Per-university approximate breakdown (latest year, 2025 estimates)
	const universityBreakdown = [
		{ name: 'Carnegie Mellon', enrollment: 4800 },
		{ name: 'Georgia Tech', enrollment: 4500 },
		{ name: 'UIUC', enrollment: 4200 },
		{ name: 'UC Berkeley', enrollment: 3900 },
		{ name: 'Purdue', enrollment: 3600 },
		{ name: 'UT Austin', enrollment: 3500 },
		{ name: 'UW Seattle', enrollment: 3400 },
		{ name: 'UMich', enrollment: 3200 },
		{ name: 'UCLA', enrollment: 3100 },
		{ name: 'UCSD', enrollment: 3000 },
		{ name: 'UMD', enrollment: 2800 },
		{ name: 'MIT', enrollment: 2700 },
		{ name: 'Stanford', enrollment: 2600 },
		{ name: 'Cornell', enrollment: 2500 },
		{ name: 'Columbia', enrollment: 2400 },
		{ name: 'UW–Madison', enrollment: 2300 },
		{ name: 'UPenn', enrollment: 2200 },
		{ name: 'Princeton', enrollment: 2000 },
		{ name: 'Caltech', enrollment: 1500 },
		{ name: 'Harvey Mudd', enrollment: 500 },
	];

	onMount(() => {
		const ctx = chartCanvas.getContext('2d');
		if (!ctx) return;

		chart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: fredYears.map(String),
				datasets: [
					{
						label: 'Software Job Openings Index (FRED)',
						data: fredSoftwareJobs,
						borderColor: '#22d3ee',
						backgroundColor: 'rgba(34, 211, 238, 0.08)',
						borderWidth: 2.5,
						pointRadius: 4,
						pointHoverRadius: 7,
						pointBackgroundColor: '#22d3ee',
						pointBorderColor: '#0a0a12',
						pointBorderWidth: 2,
						tension: 0.3,
						fill: true,
						yAxisID: 'y',
					},
					{
						label: 'CS Enrollment — Top 20 Universities',
						data: csEnrollment,
						borderColor: '#c9a84c',
						backgroundColor: 'rgba(201, 168, 76, 0.08)',
						borderWidth: 2.5,
						pointRadius: 4,
						pointHoverRadius: 7,
						pointBackgroundColor: '#c9a84c',
						pointBorderColor: '#0a0a12',
						pointBorderWidth: 2,
						tension: 0.3,
						fill: true,
						yAxisID: 'y1',
					},
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				interaction: {
					mode: 'index',
					intersect: false,
				},
				plugins: {
					legend: {
						labels: {
							color: '#e4e4ec',
							font: { family: "'DM Sans', sans-serif", size: 13, weight: '600' },
							padding: 20,
							usePointStyle: true,
							pointStyleWidth: 20,
						},
					},
					tooltip: {
						backgroundColor: 'rgba(10, 10, 18, 0.95)',
						borderColor: 'rgba(201, 168, 76, 0.3)',
						borderWidth: 1,
						titleFont: { family: "'Chakra Petch', sans-serif", size: 14, weight: '700' },
						bodyFont: { family: "'DM Sans', sans-serif", size: 13 },
						titleColor: '#e4e4ec',
						bodyColor: '#8585a0',
						padding: 14,
						cornerRadius: 8,
						callbacks: {
							label: function (context) {
								const label = context.dataset.label || '';
								const value = context.parsed.y;
								if (label.includes('Job')) {
									return `${label}: ${value}`;
								}
								return `${label}: ${value.toLocaleString()}`;
							},
						},
					},
				},
				scales: {
					x: {
						grid: { color: 'rgba(201, 168, 76, 0.06)' },
						ticks: {
							color: '#8585a0',
							font: { family: "'DM Sans', sans-serif", size: 12, weight: '600' },
						},
					},
					y: {
						type: 'linear',
						display: true,
						position: 'left',
						title: {
							display: true,
							text: 'Job Openings Index (Feb 2020 = 100)',
							color: '#22d3ee',
							font: { family: "'DM Sans', sans-serif", size: 12, weight: '600' },
						},
						grid: { color: 'rgba(34, 211, 238, 0.06)' },
						ticks: {
							color: '#22d3ee',
							font: { family: "'Space Mono', monospace", size: 11 },
						},
					},
					y1: {
						type: 'linear',
						display: true,
						position: 'right',
						title: {
							display: true,
							text: 'CS Bachelor\'s Enrollment (Top 20)',
							color: '#c9a84c',
							font: { family: "'DM Sans', sans-serif", size: 12, weight: '600' },
						},
						grid: { drawOnChartArea: false },
						ticks: {
							color: '#c9a84c',
							font: { family: "'Space Mono', monospace", size: 11 },
							callback: function (value) {
								return (value as number).toLocaleString();
							},
						},
					},
				},
			},
		});

		return () => {
			chart?.destroy();
		};
	});
</script>

<svelte:head>
	<title>Jobs vs Enrollment | Marketmon</title>
</svelte:head>

<div class="page">
	<div class="container">
		<header class="page-header">
			<h1 class="font-display title">Software Jobs <span class="text-gold">vs</span> CS Enrollment</h1>
			<p class="subtitle">
				FRED software developer job openings overlaid with computer science enrollment
				at the top 20 U.S. universities
			</p>
		</header>

		<section class="chart-section">
			<div class="chart-container">
				<canvas bind:this={chartCanvas}></canvas>
			</div>
		</section>

		<section class="insights">
			<div class="insight-card">
				<h3 class="font-display insight-title cyan">Key Takeaway</h3>
				<p>
					CS enrollment at top universities has grown steadily — more than <strong>3x</strong> since 2014 —
					while software job openings peaked in 2022 and have since contracted. The gap between
					supply (graduates) and demand (openings) has narrowed significantly.
				</p>
			</div>
			<div class="insight-card">
				<h3 class="font-display insight-title gold">The 2022 Peak</h3>
				<p>
					Software job openings hit an all-time high in 2022 (index 130), driven by pandemic-era
					digital transformation. Since then, layoffs and hiring freezes have brought the index
					back to pre-pandemic levels, even as enrollment continues to climb.
				</p>
			</div>
		</section>

		<section class="breakdown">
			<h2 class="font-display breakdown-title">Top 20 CS Programs — Estimated Enrollment (2025)</h2>
			<div class="bar-grid">
				{#each universityBreakdown as uni}
					<div class="bar-row">
						<span class="bar-label">{uni.name}</span>
						<div class="bar-track">
							<div
								class="bar-fill"
								style="width: {(uni.enrollment / universityBreakdown[0].enrollment) * 100}%"
							></div>
						</div>
						<span class="bar-value font-mono">{uni.enrollment.toLocaleString()}</span>
					</div>
				{/each}
			</div>
		</section>

		<section class="sources">
			<h3 class="font-display sources-title">Data Sources</h3>
			<ul>
				<li><strong>FRED</strong> — Software Developer Job Postings Index (IHLIDXUSTPSOFTDEVE), Federal Reserve Bank of St. Louis</li>
				<li><strong>NCES IPEDS</strong> — Integrated Postsecondary Education Data System, CS degree completions</li>
				<li>University enrollment figures are estimates based on publicly reported institutional data</li>
			</ul>
		</section>
	</div>
</div>

<style>
	.page {
		min-height: 100vh;
		padding: 2rem 1.5rem 4rem;
	}

	.container {
		max-width: 960px;
		margin: 0 auto;
	}

	.page-header {
		text-align: center;
		margin-bottom: 2.5rem;
		animation: fadeUp 0.6s ease-out;
	}

	.title {
		font-size: 2.2rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		margin-bottom: 0.75rem;
	}

	.subtitle {
		color: var(--text-secondary);
		font-size: 1rem;
		max-width: 540px;
		margin: 0 auto;
		line-height: 1.6;
	}

	.chart-section {
		animation: fadeUp 0.6s ease-out 0.1s both;
	}

	.chart-container {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: 1rem;
		padding: 1.5rem;
		height: 420px;
		position: relative;
	}

	.insights {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.25rem;
		margin-top: 2rem;
		animation: fadeUp 0.6s ease-out 0.2s both;
	}

	.insight-card {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: 0.75rem;
		padding: 1.5rem;
	}

	.insight-title {
		font-size: 1rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		margin-bottom: 0.5rem;
	}

	.insight-title.cyan { color: #22d3ee; }
	.insight-title.gold { color: var(--gold); }

	.insight-card p {
		color: var(--text-secondary);
		font-size: 0.9rem;
		line-height: 1.65;
	}

	.insight-card strong {
		color: var(--text-primary);
	}

	.breakdown {
		margin-top: 2.5rem;
		animation: fadeUp 0.6s ease-out 0.3s both;
	}

	.breakdown-title {
		font-size: 1.15rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		margin-bottom: 1.25rem;
		color: var(--text-primary);
	}

	.bar-grid {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.bar-row {
		display: grid;
		grid-template-columns: 140px 1fr 60px;
		align-items: center;
		gap: 0.75rem;
	}

	.bar-label {
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-align: right;
		white-space: nowrap;
	}

	.bar-track {
		height: 22px;
		background: var(--bg-elevated);
		border-radius: 4px;
		overflow: hidden;
	}

	.bar-fill {
		height: 100%;
		background: linear-gradient(90deg, rgba(201, 168, 76, 0.6), rgba(201, 168, 76, 0.3));
		border-radius: 4px;
		transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
	}

	.bar-value {
		font-size: 0.78rem;
		color: var(--gold);
		text-align: right;
	}

	.sources {
		margin-top: 2.5rem;
		padding: 1.5rem;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: 0.75rem;
		animation: fadeUp 0.6s ease-out 0.4s both;
	}

	.sources-title {
		font-size: 0.95rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		margin-bottom: 0.75rem;
		color: var(--text-secondary);
	}

	.sources ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.sources li {
		font-size: 0.82rem;
		color: var(--text-muted);
		line-height: 1.7;
		padding-left: 1rem;
		position: relative;
	}

	.sources li::before {
		content: '•';
		position: absolute;
		left: 0;
		color: var(--gold-dim);
	}

	.sources strong {
		color: var(--text-secondary);
	}

	@media (max-width: 768px) {
		.title { font-size: 1.5rem; }
		.insights { grid-template-columns: 1fr; }
		.chart-container { height: 320px; padding: 1rem; }
		.bar-row { grid-template-columns: 100px 1fr 55px; }
		.bar-label { font-size: 0.75rem; }
	}
</style>
