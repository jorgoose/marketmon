<script>
	import "../app.css";
</script>

<div class="app-shell">
	<div class="bg-layers" aria-hidden="true">
		<div class="bg-gradient"></div>
		<div class="bg-grid"></div>
	</div>
	<slot />
</div>

<style>
	.app-shell {
		position: relative;
		min-height: 100vh;
	}

	.bg-layers {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 0;
	}

	.bg-gradient {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(ellipse at 20% 0%, rgba(124, 58, 237, 0.08) 0%, transparent 55%),
			radial-gradient(ellipse at 80% 100%, rgba(124, 58, 237, 0.05) 0%, transparent 50%),
			radial-gradient(ellipse at 50% 30%, rgba(201, 168, 76, 0.03) 0%, transparent 50%);
	}

	/* Faint terminal grid */
	.bg-grid {
		position: absolute;
		inset: 0;
		background-image:
			repeating-linear-gradient(0deg, rgba(201, 168, 76, 0.02) 0px, transparent 1px, transparent 48px),
			repeating-linear-gradient(90deg, rgba(201, 168, 76, 0.02) 0px, transparent 1px, transparent 48px);
	}
</style>
