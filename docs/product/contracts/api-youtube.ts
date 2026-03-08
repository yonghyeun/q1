import type { ISODateTimeString, UrlString, YouTubeChannelId, YouTubeVideoId } from "./primitives";
import type { ChannelMetadata, VideoMetadata, VideoSummary } from "./domain";

/**
 * YouTube integration contract (contracts, SoT).
 *
 * 배경:
 * - 재생은 YouTube Embedded Player(IFrame)로 제공한다.
 * - 메타데이터 조회와 URL 해석은 YouTube Data API 또는 그에 준하는
 *   서버 측 integration boundary를 통해 수행한다.
 * - 이 문서는 "어떤 입력/출력이 필요한가"를 고정하고,
 *   특정 구현체(예: Next.js route, server action, 별도 proxy)는 고정하지 않는다.
 * - 현재 MVP 구현 바인딩은 `apps/web`의 Next.js route handler와
 *   `/api/youtube/*` route family를 우선 가정한다.
 *
 * 주의:
 * - 파일명 `api-youtube.ts`는 임시 명명이다.
 * - 이 파일은 request/response "형태"만 정의한다(아직 런타임 validation 없음).
 */
export interface ApiError {
  /** 머신 리더블 error code (예: `bad_request`, `upstream_error`). */
  code: string;
  /** 디버깅/로그용 메시지. */
  message: string;
}

/** 성공 응답 엔벨로프(envelope). */
export interface ApiOk<T> {
  ok: true;
  data: T;
}

/** 실패 응답 엔벨로프. UI 분기에는 안정적인 `code`를 사용한다. */
export interface ApiErr {
  ok: false;
  error: ApiError;
}

/** YouTube integration boundary에서 사용하는 표준 응답 엔벨로프. */
export type ApiResponse<T> = ApiOk<T> | ApiErr;

/**
 * 유저가 입력한 채널 URL을 canonical `channel_id`로 해석/정규화한다.
 *
 * 여러 URL 형태를 지원해야 한다(핸들/커스텀 URL 등은 추가 로직이 필요할 수 있음).
 */
export interface YouTubeResolveChannelRequest {
  channel_url: UrlString;
}

export interface YouTubeResolveChannelData {
  channel_id: YouTubeChannelId;
  /** 즉시 UI 표시에 필요한 메타데이터(필요 시 TTL 캐시 권장). */
  channel?: ChannelMetadata;
  /** (정규화를 했다면) canonical channel URL. */
  canonical_channel_url?: UrlString;
}

/** `resolve channel` integration 응답. */
export type YouTubeResolveChannelResponse = ApiResponse<YouTubeResolveChannelData>;

/** 특정 채널의 영상 목록을 조회한다(페이지네이션). */
export interface YouTubeListChannelVideosRequest {
  channel_id: YouTubeChannelId;
  page_token?: string;
  /** integration 구현체에서 페이지 사이즈 힌트로 사용할 수 있음(MVP 기본: 30). */
  page_size?: number;
}

export interface YouTubeListChannelVideosData {
  items: VideoSummary[];
  next_page_token?: string;
  prev_page_token?: string;
}

/** `list channel videos` integration 응답. */
export type YouTubeListChannelVideosResponse = ApiResponse<YouTubeListChannelVideosData>;

/** video id 배열로 메타데이터를 배치 조회한다. */
export interface YouTubeGetVideosByIdRequest {
  video_ids: YouTubeVideoId[];
}

export interface YouTubeGetVideosByIdData {
  items: VideoMetadata[];
}

/** `get videos by id` integration 응답. */
export type YouTubeGetVideosByIdResponse = ApiResponse<YouTubeGetVideosByIdData>;

/** "Video URL Open"을 위해 YouTube video URL을 `(video_id, t)`로 파싱한다. */
export interface YouTubeParseVideoUrlRequest {
  video_url: UrlString;
}

export interface YouTubeParseVideoUrlData {
  video_id: YouTubeVideoId;
  /** URL(`t=`)에서 추출한 타임스탬프(초). */
  t_seconds?: number;
  /** 표시용 `HH:MM:SS` 형태. */
  t_hms?: string;
  /** (정규화를 했다면) canonical video URL. */
  canonical_video_url?: UrlString;
  /** (파싱 과정에서 추가 조회했다면) published datetime. */
  published_at?: ISODateTimeString;
}

/** `parse video url` integration 응답. */
export type YouTubeParseVideoUrlResponse = ApiResponse<YouTubeParseVideoUrlData>;
