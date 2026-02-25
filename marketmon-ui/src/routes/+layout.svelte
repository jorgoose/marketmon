<script>
	import "../app.css";
</script>

<div class="app-shell">
	<div class="bg-decor" aria-hidden="true">
		<div class="orb orb-1"></div>
		<div class="orb orb-2"></div>
		<div class="orb orb-3"></div>
	</div>
	<slot />
</div>

<style>
	.app-shell {
		position: relative;
		min-height: 100vh;
	}

	.bg-decor {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 0;
		overflow: hidden;
	}

	.orb {
		position: absolute;
		border-radius: 50%;
		filter: blur(80px);
		opacity: 0.25;
	}

	.orb-1 {
		width: 500px;
		height: 500px;
		background: #60a5fa;
		top: -10%;
		right: -5%;
		animation: float 12s ease-in-out infinite;
	}

	.orb-2 {
		width: 400px;
		height: 400px;
		background: #fbbf24;
		bottom: 10%;
		left: -8%;
		animation: float 15s ease-in-out infinite 3s;
	}

	.orb-3 {
		width: 350px;
		height: 350px;
		background: #22c55e;
		top: 50%;
		right: 20%;
		animation: float 18s ease-in-out infinite 6s;
	}
</style>
