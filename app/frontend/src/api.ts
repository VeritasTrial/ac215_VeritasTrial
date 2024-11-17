/**
 * @file api.ts
 *
 * This file wraps the API calls to the backend server.
 */

import queryString from "query-string";
import {
  APIChatResponseType,
  APIRetrieveResponseType,
  ModelType,
  WrapAPI,
} from "./types";

/**
 * Call the /retrieve backend API.
 */
export const callRetrieve = async (
  query: string,
  topK: number,
): Promise<WrapAPI<APIRetrieveResponseType>> => {
  const params = queryString.stringify({ query, top_k: topK });
  try {
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/retrieve?${params}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const res = (await response.json()) as APIRetrieveResponseType;
    return { payload: res };
  } catch (e: unknown) {
    if (typeof e === "string") {
      return { error: e };
    } else if (e instanceof Error) {
      return { error: e.message };
    } else {
      return { error: "Unknown error" };
    }
  }
};

/**
 * Call the /chat/{model}/{item_id} backend API.
 */
export const callChat = async (
  query: string,
  model: ModelType,
  id: string,
): Promise<WrapAPI<APIChatResponseType>> => {
  const params = queryString.stringify({ query });
  try {
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/chat/${model}/${id}?${params}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const res = (await response.json()) as APIChatResponseType;
    return { payload: res };
  } catch (e: unknown) {
    if (typeof e === "string") {
      return { error: e };
    } else if (e instanceof Error) {
      return { error: e.message };
    } else {
      return { error: "Unknown error" };
    }
  }
};
