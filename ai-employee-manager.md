# AI Employee Subscription Manager

This skill manages the "Rent an AI Employee" service - handling subscriptions, user verification, and sub-agent spawning.

## What it does

1. **Verify Stripe subscriptions** - Check if user has active paid subscription
2. **Spawn sub-agents for paying users** - Each user gets their own isolated agent with memory
3. **Route Telegram messages** - Route messages to the correct user's sub-agent
4. **Handle cron reports** - Daily/weekly usage reports for each user

## Usage

### Check Subscription
```
Use skill: ai-employee-manager
Action: check_subscription
Telegram: @username
```

### Add User (after Stripe payment)
```
Use skill: ai-employee-manager  
Action: add_user
Telegram: @username
Plan: pro
```

### List Active Users
```
Use skill: ai-employee-manager
Action: list_users
```

## Configuration

Set these environment variables:
- `STRIPE_SECRET_KEY` - Your Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook signing secret
- `USERS_DB` - Path to users JSON file (default: users.json)

## Subscription Tiers

| Plan | Price | Features |
|------|-------|----------|
| Basic | $29/mo | 1 agent, 500 msgs/mo |
| Pro | $59/mo | 2 agents, unlimited, image gen |
| Enterprise | $99/mo | 5 agents, custom skills, API |

## Sub-agent Skills Available

- sales_closer
- content_marketer  
- customer_support
- research_assistant
- general_assistant
