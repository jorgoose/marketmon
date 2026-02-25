<script lang="ts">
	import { page } from '$app/stores';

	let mobileOpen = false;

	const links = [
		{ href: '/', label: 'Home' },
		{ href: '/cards', label: 'Index' },
		{ href: '/play', label: 'Arena' },
		{ href: '/about', label: 'Guide' },
	];
</script>

<header class="navbar">
	<div class="nav-inner">
		<a href="/" class="brand font-display">Marketmon</a>

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
		background: rgba(6, 6, 10, 0.85);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-bottom: 1px solid var(--border);
	}

	.nav-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
		height: 3.75rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.brand {
		font-size: 1.35rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-decoration: none;
		background: linear-gradient(135deg, #e2c56d, #c9a84c);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.nav-links {
		display: flex;
		gap: 0.125rem;
	}

	.nav-link {
		padding: 0.4rem 0.9rem;
		border-radius: 0.375rem;
		text-decoration: none;
		color: var(--text-secondary);
		font-weight: 600;
		font-size: 0.825rem;
		letter-spacing: 0.03em;
		text-transform: uppercase;
		transition: all 0.2s ease;
		border: 1px solid transparent;
	}

	.nav-link:hover {
		color: var(--text-primary);
		background: rgba(201, 168, 76, 0.06);
	}

	.nav-link.active {
		color: var(--gold);
		background: rgba(201, 168, 76, 0.08);
		border-color: rgba(201, 168, 76, 0.2);
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
		width: 22px;
		height: 2px;
		background: var(--gold);
		border-radius: 1px;
		transition: all 0.3s ease;
		transform-origin: center;
	}

	.bar.open:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
	.bar.open:nth-child(2) { opacity: 0; }
	.bar.open:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

	.mobile-nav {
		display: none;
		flex-direction: column;
		padding: 0.5rem 1.5rem 1rem;
		gap: 0.125rem;
		border-top: 1px solid var(--border);
	}

	.mobile-link {
		padding: 0.7rem 1rem;
		text-decoration: none;
		color: var(--text-secondary);
		font-weight: 600;
		font-size: 0.85rem;
		letter-spacing: 0.03em;
		text-transform: uppercase;
		border-radius: 0.375rem;
		transition: all 0.2s ease;
	}

	.mobile-link:hover,
	.mobile-link.active {
		color: var(--gold);
		background: rgba(201, 168, 76, 0.08);
	}

	@media (max-width: 768px) {
		.nav-links { display: none; }
		.mobile-toggle { display: flex; }
		.mobile-nav { display: flex; }
	}
</style>
