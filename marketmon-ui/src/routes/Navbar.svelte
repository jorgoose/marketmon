<script lang="ts">
	import { page } from '$app/stores';

	let mobileOpen = false;

	const links = [
		{ href: '/', label: 'Home' },
		{ href: '/cards', label: 'Cards' },
		{ href: '/play', label: 'Play' },
		{ href: '/about', label: 'About' },
	];
</script>

<header class="navbar">
	<div class="nav-inner">
		<a href="/" class="brand font-display">
			Marketmon
		</a>

		<nav class="nav-links">
			{#each links as link}
				<a
					href={link.href}
					class="nav-link"
					class:active={$page.url.pathname === link.href}
				>
					{link.label}
				</a>
			{/each}
		</nav>

		<button
			class="mobile-toggle"
			on:click={() => (mobileOpen = !mobileOpen)}
			aria-label="Toggle menu"
		>
			<span class="bar" class:open={mobileOpen}></span>
			<span class="bar" class:open={mobileOpen}></span>
			<span class="bar" class:open={mobileOpen}></span>
		</button>
	</div>

	{#if mobileOpen}
		<nav class="mobile-nav">
			{#each links as link}
				<a
					href={link.href}
					class="mobile-link"
					class:active={$page.url.pathname === link.href}
					on:click={() => (mobileOpen = false)}
				>
					{link.label}
				</a>
			{/each}
		</nav>
	{/if}
</header>

<style>
	.navbar {
		position: sticky;
		top: 0;
		z-index: 100;
		background: rgba(30, 64, 175, 0.7);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-bottom: 2px solid rgba(255, 255, 255, 0.1);
	}

	.nav-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
		height: 4rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.brand {
		font-size: 1.6rem;
		font-weight: 700;
		color: var(--yellow);
		text-decoration: none;
		text-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
		letter-spacing: 0.02em;
	}

	.nav-links {
		display: flex;
		gap: 0.25rem;
	}

	.nav-link {
		padding: 0.5rem 1rem;
		border-radius: 9999px;
		text-decoration: none;
		color: rgba(255, 255, 255, 0.8);
		font-weight: 700;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.nav-link:hover {
		color: #fff;
		background: rgba(255, 255, 255, 0.12);
	}

	.nav-link.active {
		color: var(--blue-deep);
		background: var(--yellow);
		box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
	}

	.mobile-toggle {
		display: none;
		flex-direction: column;
		gap: 5px;
		background: none;
		border: none;
		cursor: pointer;
		padding: 4px;
	}

	.bar {
		width: 24px;
		height: 3px;
		background: white;
		border-radius: 2px;
		transition: all 0.3s ease;
		transform-origin: center;
	}

	.bar.open:nth-child(1) { transform: rotate(45deg) translate(5px, 6px); }
	.bar.open:nth-child(2) { opacity: 0; }
	.bar.open:nth-child(3) { transform: rotate(-45deg) translate(5px, -6px); }

	.mobile-nav {
		display: none;
		flex-direction: column;
		padding: 0.5rem 1.5rem 1rem;
		gap: 0.25rem;
	}

	.mobile-link {
		padding: 0.75rem 1rem;
		text-decoration: none;
		color: rgba(255, 255, 255, 0.85);
		font-weight: 700;
		border-radius: 0.75rem;
		transition: all 0.2s ease;
	}

	.mobile-link:hover,
	.mobile-link.active {
		color: var(--blue-deep);
		background: var(--yellow);
	}

	@media (max-width: 768px) {
		.nav-links { display: none; }
		.mobile-toggle { display: flex; }
		.mobile-nav { display: flex; }
	}
</style>
