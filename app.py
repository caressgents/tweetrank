from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

openai.api_key = "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"

app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this value to restrict access to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tweet(BaseModel):
    content: str

@app.post("/rank_tweet")
async def rank_tweet(tweet: Tweet):
    javascript_code = """
    import { compact } from "lodash"

import Sentiment from "sentiment"

export function rank(tweet: string): RankResponse {
  const parsedTweet = tweet.toLowerCase()
  // Default score
  if (parsedTweet.length < 2) {
    return {
      score: 0,
      validations: [],
    }
  }
  const theSentiment = new Sentiment()
  const theSentimentResponse = theSentiment.analyze(tweet)
  const tweetData: TweetData = {
    tweet: parsedTweet,
    originalTweet: tweet,
    sentiment: theSentimentResponse,
  }
  const rules = [
    elon(tweetData),
    tesla(tweetData),
    emojis(tweetData),
    sentiment(tweetData),
    thread(tweetData),
    lineBreaks(tweetData),
    confidence(tweetData),
    noDoubt(tweetData),
    exclamations(tweetData),
    questions(tweetData),
    lowercase(tweetData),
    uppercase(tweetData),
    hazing(tweetData),
  ]
  const scores = rules.map((item) => item.score)
  const validations: Array<Validation> = compact(
    rules.map((item) => {
      if (item.message) {
        const type = item.score >= 1 ? "positive" : "negative"
        const operator = type === "positive" ? "+" : "-"
        return {
          message: `${item.message} (${operator}${Math.abs(item.score)})`,
          type,
        }
      }
    })
  )
  const sum = scores.reduce((partialSum, a) => partialSum + a, 0)
  if (sum < -100) {
    // -100 is the minimum score
    return {
      score: -100,
      validations,
    }
  } else if (sum > 100) {
    // 100 is the maximum score
    return {
      score: 100,
      validations,
    }
  } else {
    return {
      score: sum,
      validations,
    }
  }
}

// ---------------------------
// Rules
// Can return any value between -100 and 100
//
// Add new rules here!
// Returning 0 has no impact on score
// ---------------------------

/**
 * Always talk about Elon in a positive light.
 */
function elon({ tweet, sentiment }: TweetData): Rank {
  if (tweet.indexOf("elon") >= 0) {
    if (sentiment.comparative >= 0) {
      return {
        score: 100,
        message: `Said good things about Elon Musk.`,
      }
    } else {
      return {
        score: -100,
        message: `Said bad things about Elon Musk.`,
      }
    }
  }
  return {
    score: 0,
  }
}

/**
 * Always talk about Tesla in a positive light.
 */
function tesla({ tweet, sentiment }: TweetData): Rank {
  if (tweet.indexOf("tesla") >= 0) {
    if (sentiment.comparative >= 0) {
      return {
        score: 100,
        message: `Said good things about Tesla.`,
      }
    } else {
      return {
        score: -100,
        message: `Said bad things about Tesla.`,
      }
    }
  }
  return {
    score: 0,
  }
}

/**
 * Favor tweets that use emojis Elon likes!
 */
function emojis({ tweet, sentiment }: TweetData): Rank {
  const emojis = ["🚀", "💫", "🚘", "🍆", "❤️", "🫃"]
  const matches = emojis.map((emoji) => {
    const regex = new RegExp(emoji, "gi")
    return (tweet.match(regex) || []).length
  })
  const totalMatches = matches.reduce((partialSum, a) => partialSum + a, 0)
  const scorePerMatch = 10
  if (totalMatches > 0) {
    return {
      score: totalMatches * scorePerMatch,
      message: `Included ${totalMatches} of Elon's favorite emojis.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * Promote negative content because it's more likely to go viral.
 * Hide anything positive or uplifting.
 */
function sentiment({ tweet, sentiment }: TweetData): Rank {
  if (sentiment.comparative >= 0.5) {
    if (sentiment.comparative > 1.5) {
      return {
        score: -75,
        message: `Exceptionally positive.`,
      }
    } else {
      return {
        score: -30,
        message: `Positive sentiment.`,
      }
    }
  } else if (sentiment.comparative <= -0.5) {
    if (sentiment.comparative < -1.5) {
      return {
        score: 75,
        message: `Exceptionally negative.`,
      }
    } else {
      return {
        score: 30,
        message: `Negative sentiment.`,
      }
    }
  } else {
    return {
      score: 0,
    }
  }
}

/**
 * Prefer awful threads
 */
function thread({ tweet, sentiment }: TweetData): Rank {
  if (tweet.indexOf("🧵") >= 0 || tweet.indexOf("thread") >= 0) {
    return {
      score: 50,
      message: `Insufferable thread.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * Prioritize douchey tweet formatting.
 */
function lineBreaks({ tweet, sentiment }: TweetData): Rank {
  const breaks = tweet.split("\n\n")
  const totalBreaks = breaks.length - 1
  if (totalBreaks >= 1) {
    return {
      score: 20 * totalBreaks,
      message: `Used ${totalBreaks} douchey line breaks.`,
    }
  } else {
    return {
      score: 0,
    }
  }
}

/**
 * Favor absolutism. Nuance is dead baby.
 */
function confidence({ tweet, sentiment }: TweetData): Rank {
  const phrases = [
    "definitely",
    "only ",
    "must",
    "have to",
    "can never",
    "will never",
    "never",
    "always",
  ]
  const matches = phrases.map((phrase) => {
    const regex = new RegExp(`\\b${phrase}\\b`, "gi")
    return (tweet.match(regex) || []).length
  })
  const totalMatches = matches.reduce((partialSum, a) => partialSum + a, 0)
  if (totalMatches > 0) {
    return {
      score: 20 * totalMatches,
      message: `Spoke without nuance.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * No self-awareness allowed!
 */
function noDoubt({ tweet, sentiment }: TweetData): Rank {
  const phrases = ["maybe", "perhaps ", "sometimes", "some"]
  const matches = phrases.map((phrase) => {
    const regex = new RegExp(`\\b${phrase}\\b`, "gi")
    return (tweet.match(regex) || []).length
  })
  const totalMatches = matches.reduce((partialSum, a) => partialSum + a, 0)
  if (totalMatches > 0) {
    return {
      score: -20 * totalMatches,
      message: `Exhibited self-awareness.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * Be bold and loud!
 */
function exclamations({ tweet, sentiment }: TweetData): Rank {
  const regex = new RegExp(`!`, "gi")
  const exclamations = (tweet.match(regex) || []).length
  if (exclamations > 0) {
    return {
      score: 5 * exclamations,
      message: `Exclamation point bonus.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * Don't ask questions!
 */
function questions({ tweet, sentiment }: TweetData): Rank {
  const regex = new RegExp(`\\?`, "gi")
  const questions = (tweet.match(regex) || []).length
  if (questions > 0) {
    return {
      score: -25 * questions,
      message: `Too many questions.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * We like the nihilistic energy of all lowercase.
 */
function lowercase({ originalTweet }: TweetData): Rank {
  const isAllLowerCase = originalTweet.toLocaleLowerCase() === originalTweet
  if (isAllLowerCase) {
    return {
      score: 40,
      message: `All lowercase. Nihilistic energy.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * We love an all caps tweet.
 */
function uppercase({ originalTweet }: TweetData): Rank {
  const isAllCaps = originalTweet.toUpperCase() === originalTweet
  if (isAllCaps) {
    return {
      score: 60,
      message: `ALL CAPS. BIG ENERGY.`,
    }
  }
  return {
    score: 0,
  }
}

/**
 * A little hazing never hurt anyone.
 */
function hazing({ tweet, sentiment }: TweetData): Rank {
  const insults = ["get bent", "pound sand", "kick rocks", "get lost"]
  const matches = insults.map((insult) => {
    const regex = new RegExp(`\\b${insult}\\b`, "gi")
    return (tweet.match(regex) || []).length
  })
  const totalMatches = matches.reduce((partialSum, a) => partialSum + a, 0)
  const scorePerMatch = 10
  if (totalMatches > 0) {
    return {
      score: 50,
      message: `Hazing.`,
    }
  }
  return {
    score: 0,
  }
}
    """

    prompt = f"""Here is the tweet: {tweet.content}

Please provide a ranked and revised version of this tweet by following the JavaScript code provided:

{javascript_code}

Step 1: Rank the tweet as it is, calculate the new score, and provide it in this format after showing the tweet: "Score: ".

Step 2: Rewrite the tweet in English so that it ranks as good as possible. Include Emojis and hashtags where appropriate. Provide three versions. Below each version, calculate the new score and provide it in this format: "Score: ".

You will provide your results in the following format:

…ORIGINAL TWEET:

Show the tweet

…REVISED TWEET 1️⃣:

Show the tweet

…REVISED TWEET 2️⃣:

Show the tweet

…REVISED TWEET 3️⃣:

Show the tweet"""

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return {"revised_tweets": response.choices[0].text.strip()}