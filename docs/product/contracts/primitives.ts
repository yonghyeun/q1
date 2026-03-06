/**
 * Unix epoch(UTC) 기준 밀리초(ms).
 *
 * `Date` 직렬화/타임존 모호성을 피하기 위해 analytics/storage 전반에서 사용한다.
 */
export type UnixMillis = number;

/**
 * ISO 8601 datetime 문자열 (예: `2026-03-05T12:34:56Z`).
 *
 * 참고: YouTube Data API는 RFC3339 타임스탬프를 반환한다. 여기서는 같은 형태로 유지한다.
 */
export type ISODateTimeString = string;

/** 절대 URL 문자열. 당장은 string으로 두고, 경계(API/입력)에서 검증한다. */
export type UrlString = string;

/** SemVer 문자열 (예: `1.2.3`). */
export type SemVerString = string;

/**
 * MVP용 익명 유저 식별자(로그인 없음).
 *
 * 보통 1회 생성 후 LocalStorage에 저장한다.
 */
export type UserId = string;

/** analytics에서 이벤트를 묶기 위한 세션 식별자. */
export type SessionId = string;

/** analytics 공통 프로퍼티에 넣는 앱 버전 문자열. */
export type AppVersion = SemVerString;

/** YouTube video id (`v=` 파라미터 값). */
export type YouTubeVideoId = string;

/** YouTube channel id (예: `UC...`). */
export type YouTubeChannelId = string;

/** YouTube playlist id. Post-MVP에서 `PlaylistSource`에 사용할 수 있다. */
export type YouTubePlaylistId = string;

/**
 * API에서 가져온 데이터(예: YouTube 메타데이터)를 TTL로 캐시하기 위한 래퍼.
 *
 * 정책 메모: YouTube API Data(타이틀/썸네일 등)를 무기한 저장하는 것은 안전하지 않으므로,
 * TTL + 주기적 갱신(또는 필요 시 재조회) 형태를 선호한다.
 */
export interface TtlCacheEntry<T> {
  value: T;
  fetched_at: UnixMillis;
  expires_at: UnixMillis;
}
